import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from jinja2 import Template
from pydantic import EmailStr
from functools import lru_cache

class EmailService:
    def __init__(self):
        """
        メールサービスの初期化
        環境変数から設定を読み込む
        """
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.default_sender = os.getenv("DEFAULT_SENDER_EMAIL")

    def _create_smtp_connection(self) -> smtplib.SMTP:
        """
        SMTPサーバーへの接続を確立
        """
        smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
        smtp.starttls()
        smtp.login(self.smtp_username, self.smtp_password)
        return smtp

    @lru_cache(maxsize=10)
    def _load_template(self, template_name: str) -> Template:
        """
        メールテンプレートを読み込む
        """
        template_path = f"app/templates/emails/{template_name}.html"
        with open(template_path, "r") as f:
            return Template(f.read())

    async def send_email(
        self,
        to_email: EmailStr,
        subject: str,
        body: str,
        cc: Optional[List[EmailStr]] = None,
        bcc: Optional[List[EmailStr]] = None,
        is_html: bool = False
    ) -> bool:
        """
        メールを送信する基本機能
        
        Args:
            to_email: 送信先メールアドレス
            subject: メールの件名
            body: メール本文
            cc: CCに追加するメールアドレスのリスト
            bcc: BCCに追加するメールアドレスのリスト
            is_html: HTMLメールかどうか
        
        Returns:
            bool: 送信成功の場合True
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = self.default_sender
            msg["To"] = to_email
            msg["Subject"] = subject

            if cc:
                msg["Cc"] = ", ".join(cc)
            if bcc:
                msg["Bcc"] = ", ".join(bcc)

            content_type = "html" if is_html else "plain"
            msg.attach(MIMEText(body, content_type))

            with self._create_smtp_connection() as smtp:
                recipients = [to_email]
                if cc:
                    recipients.extend(cc)
                if bcc:
                    recipients.extend(bcc)
                smtp.send_message(msg, to_addrs=recipients)

            return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    async def send_welcome_email(self, to_email: EmailStr, username: str) -> bool:
        """
        ユーザー登録時のウェルカムメールを送信
        """
        template = self._load_template("welcome")
        body = template.render(username=username)
        return await self.send_email(
            to_email=to_email,
            subject="Welcome to SpeakPro!",
            body=body,
            is_html=True
        )

    async def send_lesson_confirmation(
        self,
        to_email: EmailStr,
        lesson_details: dict
    ) -> bool:
        """
        レッスン予約確認メールを送信
        """
        template = self._load_template("lesson_confirmation")
        body = template.render(**lesson_details)
        return await self.send_email(
            to_email=to_email,
            subject="Lesson Confirmation",
            body=body,
            is_html=True
        )

    async def send_password_reset(
        self,
        to_email: EmailStr,
        reset_token: str,
        expiry_time: str
    ) -> bool:
        """
        パスワードリセットメールを送信
        """
        template = self._load_template("password_reset")
        reset_url = f"{os.getenv('FRONTEND_URL')}/reset-password?token={reset_token}"
        body = template.render(reset_url=reset_url, expiry_time=expiry_time)
        return await self.send_email(
            to_email=to_email,
            subject="Password Reset Request",
            body=body,
            is_html=True
        )

# シングルトンインスタンスの作成
email_service = EmailService()
# 基本的な使用例
await email_service.send_email(
    to_email="user@example.com",
    subject="Test Email",
    body="This is a test email"
)

# ウェルカムメールの送信
await email_service.send_welcome_email(
    to_email="newuser@example.com",
    username="John Doe"
)