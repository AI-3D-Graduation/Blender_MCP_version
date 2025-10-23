"""
Blender MCP Server Addon (Socket Server)
Blender가 포트에서 대기하고 MCP 서버가 연결
"""
import bpy
import socket
import threading
import json
import time
from queue import Queue

# Blender 소켓 서버 정보
HOST = 'localhost'
PORT = 9876  # Blender 애드온 포트 (MCP가 여기에 연결)

# 명령 큐 (메인 스레드에서 처리)
command_queue = Queue()
response_queue = {}  # request_id -> response


class BlenderMCPServer:
    def __init__(self):
        self.server_socket = None
        self.running = False
        self.connections = []  # 활성 연결 리스트
        
    def start(self):
        """Blender에서 소켓 서버 시작 (MCP가 여기에 연결)"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(5)
            self.running = True
            print(f"✅ Blender listening on {HOST}:{PORT} (waiting for MCP connection)")
            
            while self.running:
                try:
                    self.server_socket.settimeout(1.0)
                    conn, addr = self.server_socket.accept()
                    print(f"✅ MCP connected from {addr}")
                    
                    # 연결 처리를 별도 스레드에서
                    threading.Thread(target=self.handle_mcp_connection, args=(conn,), daemon=True).start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"❌ Error: {e}")
                        
        except Exception as e:
            print(f"❌ Failed to start Blender server: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def handle_mcp_connection(self, conn):
        """MCP 서버로부터의 연결 처리"""
        self.connections.append(conn)
        try:
            while True:
                data = conn.recv(8192)
                if not data:
                    break
                    
                # MCP 명령 처리
                try:
                    message = data.decode('utf-8').strip()
                    print(f"📩 Received from MCP: {message[:100]}...")
                    
                    # JSON-RPC 파싱
                    try:
                        request = json.loads(message)
                        method = request.get('method', 'unknown')
                        params = request.get('params', {})
                        request_id = request.get('id')
                        
                        print(f"📋 Command: {method}, Params: {params}")
                        
                        # 명령을 큐에 추가 (메인 스레드에서 처리)
                        command_queue.put({
                            'request_id': request_id,
                            'method': method,
                            'params': params,
                            'conn': conn
                        })
                        
                        print(f"📝 Command queued, waiting for processing...")
                        
                    except json.JSONDecodeError as e:
                        # JSON 파싱 오류
                        error_response = json.dumps({
                            "jsonrpc": "2.0",
                            "id": None,
                            "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
                        }) + "\n"
                        conn.sendall(error_response.encode('utf-8'))
                    
                except Exception as e:
                    print(f"❌ Error processing message: {e}")
                    error_response = json.dumps({
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
                    })
                    try:
                        conn.sendall(error_response.encode('utf-8'))
                    except:
                        pass
                    
        except Exception as e:
            print(f"❌ Connection handler error: {e}")
        finally:
            if conn in self.connections:
                self.connections.remove(conn)
            conn.close()
            print("🔌 MCP disconnected")
    
    def execute_command(self, method: str, params: dict) -> dict:
        """Blender 명령 실행"""
        try:
            if method == "load_model":
                file_path = params.get("file_path", "")
                print(f"📂 Loading model: {file_path}")
                
                # Blender에서 모델 로드
                bpy.ops.object.select_all(action='SELECT')
                bpy.ops.object.delete()
                
                if file_path.endswith('.glb') or file_path.endswith('.gltf'):
                    bpy.ops.import_scene.gltf(filepath=file_path)
                    return {"status": "success", "message": f"Model loaded: {file_path}"}
                else:
                    return {"status": "error", "message": "Unsupported file format"}
            
            elif method == "execute_edit":
                command = params.get("command", "")
                edit_params = params.get("params", {})
                print(f"✏️ Executing edit: {command}")
                print(f"✏️ Params: {edit_params}")
                
                # 선택된 모든 객체에 대해 편집 실행
                selected_objects = bpy.context.selected_objects
                if not selected_objects:
                    # 모든 메쉬 객체 선택
                    for obj in bpy.data.objects:
                        if obj.type == 'MESH':
                            obj.select_set(True)
                    selected_objects = bpy.context.selected_objects
                
                # 명령별 처리
                if command == "change_color":
                    r = edit_params.get("r", 0.0)
                    g = edit_params.get("g", 0.3)
                    b = edit_params.get("b", 1.0)
                    a = edit_params.get("a", 1.0)
                    print(f"🎨 Applying color: R={r}, G={g}, B={b}, A={a}")
                    self.change_object_color(selected_objects, (r, g, b, a))
                    return {"status": "success", "message": f"색상이 변경되었습니다"}
                
                elif command == "add_object":
                    obj_type = edit_params.get("type", "CUBE")
                    position = edit_params.get("position", [0, 0, 0])
                    scale = edit_params.get("scale", 1.0)
                    
                    # 객체 추가
                    if obj_type == "CUBE":
                        bpy.ops.mesh.primitive_cube_add(location=position, scale=(scale, scale, scale))
                    elif obj_type == "SPHERE":
                        bpy.ops.mesh.primitive_uv_sphere_add(location=position, radius=scale)
                    elif obj_type == "CYLINDER":
                        bpy.ops.mesh.primitive_cylinder_add(location=position, radius=scale)
                    elif obj_type == "CONE":
                        bpy.ops.mesh.primitive_cone_add(location=position, radius1=scale)
                    
                    new_obj = bpy.context.active_object
                    return {"status": "success", "message": f"{obj_type}가 추가되었습니다"}
                
                elif command == "scale_model":
                    factor = edit_params.get("factor", 1.0)
                    for obj in selected_objects:
                        obj.scale *= factor
                    return {"status": "success", "message": f"크기를 {factor}배로 변경했습니다"}
                
                elif command == "rotate_model":
                    axis = edit_params.get("axis", "Z")
                    angle = edit_params.get("angle", 90)
                    import math
                    angle_rad = math.radians(angle)
                    
                    for obj in selected_objects:
                        if axis == "X":
                            obj.rotation_euler[0] += angle_rad
                        elif axis == "Y":
                            obj.rotation_euler[1] += angle_rad
                        elif axis == "Z":
                            obj.rotation_euler[2] += angle_rad
                    
                    return {"status": "success", "message": f"{axis}축으로 {angle}도 회전했습니다"}
                
                elif command == "apply_smooth":
                    for obj in selected_objects:
                        if obj.type == 'MESH':
                            bpy.context.view_layer.objects.active = obj
                            bpy.ops.object.shade_smooth()
                    return {"status": "success", "message": "스무딩이 적용되었습니다"}
                
                elif command == "subdivide":
                    levels = edit_params.get("levels", 2)
                    for obj in selected_objects:
                        if obj.type == 'MESH':
                            # Subdivision Surface 모디파이어 추가
                            mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
                            mod.levels = levels
                            mod.render_levels = levels
                    return {"status": "success", "message": f"레벨 {levels}로 세분화했습니다"}
                
                elif command == "change_material":
                    metallic = edit_params.get("metallic", 0.0)
                    roughness = edit_params.get("roughness", 0.5)
                    
                    for obj in selected_objects:
                        if obj.type == 'MESH' and obj.data.materials:
                            mat = obj.data.materials[0]
                            if mat.use_nodes:
                                bsdf = mat.node_tree.nodes.get("Principled BSDF")
                                if bsdf:
                                    bsdf.inputs['Metallic'].default_value = metallic
                                    bsdf.inputs['Roughness'].default_value = roughness
                    
                    return {"status": "success", "message": f"재질을 변경했습니다 (Metallic: {metallic}, Roughness: {roughness})"}
                
                else:
                    return {"status": "success", "message": f"명령을 수신했습니다: {command}"}
            
            elif method == "export_model":
                file_path = params.get("file_path", "")
                format_type = params.get("format", "GLB")
                print(f"💾 Exporting model: {file_path}")
                
                if format_type == "GLB":
                    bpy.ops.export_scene.gltf(filepath=file_path, export_format='GLB')
                    return {"status": "success", "message": f"Model exported: {file_path}"}
                else:
                    return {"status": "error", "message": "Unsupported export format"}
            
            else:
                return {"status": "error", "message": f"Unknown method: {method}"}
                
        except Exception as e:
            print(f"❌ Command execution error: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": str(e)}
    
    def change_object_color(self, objects, color_rgba):
        """객체의 색상 변경"""
        for obj in objects:
            if obj.type == 'MESH':
                print(f"🎨 Changing color for object: {obj.name}")
                
                # 기존 재질이 있으면 모두 제거
                obj.data.materials.clear()
                
                # 새 재질 생성
                mat = bpy.data.materials.new(name=f"Material_{obj.name}")
                mat.use_nodes = True
                obj.data.materials.append(mat)
                
                # 노드 트리 가져오기
                nodes = mat.node_tree.nodes
                links = mat.node_tree.links
                
                # 기존 노드 모두 제거
                nodes.clear()
                
                # Principled BSDF 노드 생성
                bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
                bsdf.location = (0, 0)
                
                # Material Output 노드 생성
                output = nodes.new(type='ShaderNodeOutputMaterial')
                output.location = (400, 0)
                
                # 노드 연결
                links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
                
                # 색상 적용
                bsdf.inputs['Base Color'].default_value = color_rgba
                bsdf.inputs['Metallic'].default_value = 0.0
                bsdf.inputs['Roughness'].default_value = 0.5
                
                print(f"✅ Color applied to {obj.name}: RGBA={color_rgba}")
    
    def stop(self):
        """서버 중지"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()

# 서버 인스턴스 생성 및 시작
if __name__ == "__main__":
    blender_mcp_server = BlenderMCPServer()
    server_thread = threading.Thread(target=blender_mcp_server.start, daemon=True)
    server_thread.start()
    print("🚀 Blender MCP Server started in background")
    print(f"⏳ Waiting for MCP to connect on port {PORT}...")
    
    # 메인 스레드에서 명령 처리를 위한 타이머 등록
    def process_commands():
        """메인 스레드에서 명령 큐 처리"""
        while not command_queue.empty():
            try:
                cmd = command_queue.get_nowait()
                request_id = cmd['request_id']
                method = cmd['method']
                params = cmd['params']
                conn = cmd['conn']
                
                print(f"⚙️ Processing command in main thread: {method}")
                
                # Blender 명령 실행 (메인 스레드에서만 가능)
                result = blender_mcp_server.execute_command(method, params)
                
                # 응답 전송
                response = json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }) + "\n"
                
                try:
                    conn.sendall(response.encode('utf-8'))
                    print(f"✅ Response sent: {response[:100]}...")
                except Exception as e:
                    print(f"❌ Failed to send response: {e}")
                    
            except Exception as e:
                print(f"❌ Error processing command: {e}")
                import traceback
                traceback.print_exc()
        
        return 0.1  # 0.1초마다 재실행
    
    # Blender 타이머 등록 (메인 스레드에서 주기적으로 실행)
    bpy.app.timers.register(process_commands, first_interval=0.1)
