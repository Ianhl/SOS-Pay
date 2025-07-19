import pyotp
from datetime import datetime, timedelta

def send_otp(request):
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=60)
    otp = totp.now()

    request.session['otp_secret_key'] = secret
    request.session['otp_valid_date'] = (datetime.now() + timedelta(minutes=5)).isoformat()

    return otp
    