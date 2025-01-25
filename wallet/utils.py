import random
import pyotp
from datetime import datetime, timedelta

def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    return totp.now()

def verify_otp(otp, transaction_otp):
    return otp == transaction_otp
    