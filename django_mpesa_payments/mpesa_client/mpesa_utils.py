# mpeas_client/mpesa_utils.py
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import base64
from datetime import datetime
import logging
import os
from rest_framework.response import Response



# Configure logging
logger = logging.getLogger(__name__)

def get_mpesa_token():
    url =  'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

 
    
    # Log the URL to ensure it is being read correctly
    logger.debug(f"Requesting token from URL: {url}")

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


logger = logging.getLogger(__name__)

def lipa_na_mpesa_online(phone_number, amount):
    access_token = get_mpesa_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
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
        "CallBackURL": "https://rycha-pay.onrender.com/payments/confirmation/",
        "AccountReference": "rycha goods",
        "TransactionDesc": "Payment for goods"
    }

    response = requests.post(api_url, json=payload, headers=headers)

    # Log the response status code and content
    logger.info("Response status code: %s", response.status_code)
    logger.info("Response content: %s", response.text)

    # Check if the response is empty
    if not response.text:
        logger.error("Empty response received")
        return None  # Handle the empty response case

    # Check if the response content type is JSON
    if 'application/json' not in response.headers.get('Content-Type', ''):
        logger.error("Non-JSON response received: %s", response.text)
        return None  # Handle the non-JSON response case

    try:
        return response.json()
    except ValueError as e:
        logger.error("Error parsing JSON: %s", e)
        return None  # Or handle the error as needed

        