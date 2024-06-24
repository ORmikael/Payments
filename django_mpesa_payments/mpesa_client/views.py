import json
from django.shortcuts import render


# mpesa_client/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from .models import MpesaTransaction
from .mpesa_utils import lipa_na_mpesa_online

from django.views.decorators.csrf import csrf_exempt

# create a comprehensive function to  convert phone numbers into a valid format bore sending an api request to daraja 

# import re


# # validate phone number first
# def validate_and_format_phone_number(phone_number):
#     phone_number = phone_number.strip()
    
#     # Regex patterns
#     pattern_10_digits = r'^(07|01)\d{8}$'
#     pattern_13_digits = r'^\+254(7|1)\d{8}$'
#     pattern_12_digits = r'^254(7|1)\d{8}$'
    
#     valid_phone_number = None
    
#     if re.match(pattern_10_digits, phone_number):
#         valid_phone_number = '254' + phone_number[1:]
#     elif re.match(pattern_13_digits, phone_number):
#         valid_phone_number = phone_number[1:]
#     elif re.match(pattern_12_digits, phone_number):
#         valid_phone_number = phone_number
#     else:
#         raise ValueError("Invalid phone number format")
    
#     return valid_phone_number




# view to initiate payment 
@csrf_exempt
def pay(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
# validate the phone number before sending a request to daraja api 
        # try:
        #     valid_phone_number = validate_and_format_phone_number(phone_number)
        # except ValueError as e:
        #     return JsonResponse({'error': 'Invalid phone number format', 'invalid_phone_number': phone_number}, status=400)



        response = lipa_na_mpesa_online(phone_number, amount)
        return JsonResponse(response)
    return render(request, 'init_payment.html')


# view to confirm payment 
@csrf_exempt


# view to save the payment transaction data
@csrf_exempt
def payment_confirmation(request):
    if request.method == 'POST':
        mpesa_body = json.loads(request.body.decode('utf-8'))
        
        # Extract transaction information from the response
        transaction_id = mpesa_body.get('TransactionID', '')
        amount = mpesa_body.get('Amount', 0)
        phone_number = mpesa_body.get('PhoneNumber', '')
        transaction_date = mpesa_body.get('TransactionDate', '')
        status = mpesa_body.get('ResultDesc', 'Failed')
        
        # Save the transaction information to the database
        MpesaTransaction.objects.create(
            transaction_id=transaction_id,
            amount=amount,
            phone_number=phone_number,
            transaction_date=transaction_date,
            status=status,
            additional_info=json.dumps(mpesa_body)
        )
        
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    return HttpResponse("Only POST method is allowed", status=405)

# view to render the payment confirmation page 
# @csrf_exempt
def confirm_payment(request):
#     # Get the latest transaction information
#     latest_transaction = MpesaTransaction.objects.latest('transaction_date')
    
#     context = {
#         'transaction': latest_transaction
#     }
    
#     return render(request, 'confirm_payment.html', context)
    return