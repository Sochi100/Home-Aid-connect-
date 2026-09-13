import requests
from django.conf import settings
from django.core.mail import send_mail


def send_termii_otp(phone_number, otp_code):
    base_url = getattr(
        settings,
        "TERMII_BASE_URL",
        "https://api.ng.termii.com/api"
    ).rstrip('/')
    url = f"{base_url}/sms/send"

    formatted_phone = str(phone_number).replace("+", "").strip()

    payload = {
        "to": formatted_phone,
        "from": getattr(settings, "TERMII_SENDER_ID", "N-ALERT"),
        "sms": f"Your HomeAid Connect verification code is {otp_code}. Valid for 10 minutes.",
        "type": "plain",
        "channel": "dnd",
        "api_key": getattr(settings, "TERMII_API_KEY", ""),
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"Termii HTTP Status: {response.status_code}")
        print(f"Termii Raw Response: {response.text}")
        return response.json() if response.text else {}
    except requests.exceptions.RequestException as e:
        print(f"Termii SMS Network Error: {e}")
        return None


def send_email_otp(user_email, otp_code):
    subject = "HomeAid Connect - Verification Code"
    message = f"Your verification code is: {otp_code}\n\nValid for 10 minutes."
    html_message = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
        <h2>Welcome to HomeAid Connect</h2>
        <p>Your 6-digit verification code is:</p>
        <h1 style="color: #2563eb; letter-spacing: 4px;">{otp_code}</h1>
        <p>This code is valid for <strong>10 minutes</strong>. Do not share this code with anyone.</p>
    </div>
    """
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", getattr(settings, "EMAIL_HOST_USER", ""))

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Email OTP successfully sent via SMTP to {user_email}")
        return True
    except Exception as e:
        print(f"SMTP Email Error: {e}")
        return False