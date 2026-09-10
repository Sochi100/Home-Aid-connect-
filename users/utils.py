import requests
from django.conf import settings


def send_termii_otp(phone_number, otp_code):
    base_url = getattr(
        settings,
        "TERMII_BASE_URL",
        "https://api.ng.termii.com/api"
    )
    url = f"{base_url}/sms/send"

    # Format phone number for Termii (remove leading '+')
    formatted_phone = str(phone_number).replace("+", "").strip()

    payload = {
        "to": formatted_phone,
        "from": getattr(settings, "TERMII_SENDER_ID", "N-ALERT"),
        "sms": (
            f"Your HomeAid Connect verification code is {otp_code}. "
            f"Valid for 10 minutes."
        ),
        "type": "plain",
        "channel": "generic",
        "api_key": getattr(settings, "TERMII_API_KEY", ""),
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Termii SMS Error: {e}")
        return None