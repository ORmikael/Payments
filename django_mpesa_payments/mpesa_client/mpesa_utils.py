# mpeas_client/mpesa_utils.py
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import base64
from datetime import datetime
import logging


# Configure logging
logger = logging.getLogger(__name__)

def get_mpesa_token():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    try:
        response = requests.get(url, auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))

        # Log status code and headers
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")

        # Log response content
        logger.debug(f"Response content: {response.text}")

        # Check if the response contains valid JSON
        try:
            token = response.json().get('access_token')
            if token:
                return token
            else:
                logger.error("Access token not found in the response.")
                raise ValueError("Access token not found in the response.")
        except ValueError as e:
            logger.error(f"JSON decoding error: {e}")
            raise

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise



def lipa_na_mpesa_online(phone_number, amount):
    access_token = get_mpesa_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()).decode('utf-8')


    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://rycha-pay.onrender.com//payments/confirmation/",
        "AccountReference": "Test123",
        "TransactionDesc": "Payment for goods"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
