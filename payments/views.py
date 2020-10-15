from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from datetime import datetime

import os
from pathlib import Path
#from mysite.settings import BASE_DIR
from .checksum import *

BASE_DIR = Path(__file__).resolve().parent.parent
secret_key = os.environ.get('ZAAKPAY_SECRET_KEY')
Merchant_ID = os.environ.get('ZAAKPAY_MERCHANT_ID')
response_url = os.environ.get('response_url')
#print(BASE_DIR)
postdata = {}

def generatePostdata():
    # Should generate the following values dynamically in Production
    postdata = {}
    postdata['merchantIdentifier'] = Merchant_ID
    postdata['returnUrl'] = response_url
    postdata['txnType'] = '1'
    postdata['zpPayOption'] = '1'
    postdata['mode'] = '0'
    postdata['currency'] = 'INR'
    postdata['purpose'] = '1'
    postdata['productDescription'] = 'test product'
    postdata['debitorcredit'] = 'wallet'
    postdata['orderId'] = datetime.now().strftime('%m%H%d%M%Y%S')  # generates unique order ID
    postdata['txnDate'] = datetime.now().strftime('%Y-%m-%d')  # generate current date in YYYY-MM-DD format
    
    return postdata


def payment_page(request):
    if request.method == 'GET':
        return render(request, 'merchant.html')


def posttozaakpay(request):
    
    postdata = generatePostdata()
    
    mandatory_params = ['amount','buyerEmail','currency','merchantIdentifier','orderId']
    
    if request.method == 'POST':
        #postdata = generatePostdata()
        data = request.POST
        
        for key in data:
            postdata[key] = data[key]
        
        for key in mandatory_params:
            if postdata[key] == '':
                messages.error(request, "Please fill in the Required Details")
                return redirect('payment_page')          
    
        checksum = Checksum(postdata) # creating Checksum object
        alldata = checksum.get_allParams()
        checksum_value = checksum.calculate_checksum(secret_key, alldata)
        param_dict= checksum.output_form(checksum_value)
        
        return render(request, 'posttozaakpay.html', {'param_dict':param_dict})
        
    
@csrf_exempt  # Have to exempt csrf cause we are recieving data from zaakpay 
def response(request):  # handles zaakpay response
    if request.method == 'POST':
        response_dict = {}
        data = request.POST
        for key in data:
            response_dict[key] = data[key]
    
    recvd_checksum = data['checksum']
    
    checksum = Checksum(response_dict)
    alldata = checksum.get_allResponseParams()
    checksum_check = checksum.verify_checksum(recvd_checksum, secret_key, alldata)
    
    response_out = {}
    response_out['orderId'] = response_dict['orderId']
    response_out['transaction_status'] = response_dict['responseDescription']
    response_out['Checksum Verified?'] = checksum_check
    
    return render(request, 'response.html', {'response_out':response_out})


