from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)


async def send_result_email(recipient_email: str, viewer_url: str):

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f4f4;">
        <div style="width: 100%; max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); overflow: hidden;">
            <div style="padding: 40px 30px; text-align: center;">
                
                <h1 style="color: #333333; font-size: 24px; margin-top: 0; margin-bottom: 20px;">3D 모델 생성이 완료되었습니다!</h1>
                
                <p style="color: #555555; font-size: 16px; line-height: 1.6;">
                    요청하신 이미지의 3D 모델 변환이 성공적으로 완료되었습니다.<br>
                    아래 버튼을 클릭하여 생성된 3D 모델을 확인해 보세요.
                </p>
                
                <a href="{viewer_url}" target="_blank" style="display: inline-block; background-color: #007bff; color: #ffffff; padding: 12px 24px; margin: 30px 0; font-size: 16px; font-weight: bold; text-decoration: none; border-radius: 5px;">
                    3D 모델 확인하기
                </a>
                
                <p style="color: #777777; font-size: 14px;">
                    이 링크는 24시간 동안 유효합니다. (예시 문구)
                </p>

            </div>
            <div style="background-color: #f9f9f9; padding: 20px 30px; text-align: center; border-top: 1px solid #eeeeee;">
                <p style="color: #aaaaaa; font-size: 12px; margin: 0;">
                    &copy; 2025 Your Project Name. All Rights Reserved.
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    message = MessageSchema(
        subject="[알림] 요청하신 3D 모델 생성이 완료되었습니다.",
        recipients=[recipient_email],
        body=html_content,
        subtype="html"
    )

    try:
        fm = FastMail(conf)
        await fm.send_message(message)
        print(f"결과 이메일 전송 성공: {recipient_email}")
        return True, "Email sent successfully."
    except Exception as e:
        print(f"결과 이메일 전송 실패: {recipient_email}, 원인: {e}")
        return False, str(e)