import React, { useState, useRef, useEffect } from 'react';
import { blenderApi } from '../../entities/api/blenderApi';
import './BlenderChat.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  toolsUsed?: any[];
}

interface BlenderChatProps {
  taskId: string;
  onModelUpdated?: (modelUrl: string) => void;
}

export const BlenderChat: React.FC<BlenderChatProps> = ({ taskId, onModelUpdated }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: '안녕하세요! 3D 모델을 어떻게 편집해드릴까요? 예: "모델을 더 부드럽게 만들어줘", "색상을 파란색으로 바꿔줘"',
      timestamp: new Date(),
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await blenderApi.editWithChat(taskId, input);

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
        toolsUsed: response.tools_used,
      };

      setMessages(prev => [...prev, assistantMessage]);

      // 모델이 업데이트되었으면 부모 컴포넌트에 알림
      if (response.model_url && onModelUpdated) {
        onModelUpdated(response.model_url);
      }
    } catch (error: any) {
      const errorMessage: Message = {
        role: 'assistant',
        content: `오류가 발생했습니다: ${error.response?.data?.detail || error.message}`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleReset = async () => {
    try {
      await blenderApi.resetConversation(taskId);
      setMessages([
        {
          role: 'assistant',
          content: '대화가 초기화되었습니다. 새로운 편집을 시작해주세요!',
          timestamp: new Date(),
        }
      ]);
    } catch (error) {
      console.error('Failed to reset conversation:', error);
    }
  };

  return (
    <div className="blender-chat-container">
      <div className="chat-header">
        <h3>🎨 Blender AI 편집</h3>
        <button onClick={handleReset} className="reset-btn">
          대화 초기화
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-content">
              <div className="message-text">{msg.content}</div>
              {msg.toolsUsed && msg.toolsUsed.length > 0 && (
                <div className="tools-used">
                  <details>
                    <summary>사용된 도구 ({msg.toolsUsed.length}개)</summary>
                    <ul>
                      {msg.toolsUsed.map((tool, i) => (
                        <li key={i}>
                          <strong>{tool.tool}</strong>
                          {tool.success ? ' ✅' : ' ❌'}
                        </li>
                      ))}
                    </ul>
                  </details>
                </div>
              )}
            </div>
            <div className="message-time">
              {msg.timestamp.toLocaleTimeString('ko-KR', { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="편집 요청을 입력하세요... (예: 모델을 더 부드럽게 만들어줘)"
          disabled={isLoading}
          rows={2}
        />
        <button 
          onClick={handleSend} 
          disabled={!input.trim() || isLoading}
          className="send-btn"
        >
          {isLoading ? '처리중...' : '전송'}
        </button>
      </div>

      <div className="chat-examples">
        <p>💡 편집 예시:</p>
        <div className="example-chips">
          <button onClick={() => setInput('모델을 더 부드럽게 만들어줘')}>
            부드럽게
          </button>
          <button onClick={() => setInput('색상을 파란색으로 바꿔줘')}>
            색상 변경
          </button>
          <button onClick={() => setInput('모델 크기를 2배로 키워줘')}>
            크기 조정
          </button>
          <button onClick={() => setInput('금속 재질로 바꿔줘')}>
            재질 변경
          </button>
        </div>
      </div>
    </div>
  );
};
