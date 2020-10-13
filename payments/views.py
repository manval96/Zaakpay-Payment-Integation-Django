from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
from decouple import config
#config.encoding='base64_codec'
from .checksum import *

secret_key = os.environ.get('ZAAKPAY_SECRET_KEY')
Merchant_ID = os.environ.get('ZAAKPAY_MERCHANT_ID') #config('ZAAKPAY_MERCHENT_KEY')

def payment_page(request):
    return render(request, 'merchant.html')


def posttozaakpay(request):
    
    if request.method == 'POST':
        postdata = {}
        data = request.POST
        for key in data:
            postdata[key] = data[key]
    
    postdata['merchantIdentifier'] = Merchant_ID
    
    checksum = Checksum(postdata) # creating Checksum object
    alldata = checksum.get_allParams()
    checksum_value = checksum.calculate_checksum(secret_key, alldata)
    param_dict= checksum.output_form(checksum_value)
    
    return render(request, 'posttozaakpay.html', {'param_dict':param_dict})
        
    
@csrf_exempt # Have to exempt csrf cause we are recieving data from zaakpay 
def response(request): # handles zaakpay response
    if request.method == 'POST':
        response_dict = {}
        data = request.POST
        for key in data:
            response_dict[key] = data[key]
    
    recvd_checksum = data['checksum']
    
    checksum = Checksum(response_dict)
    alldata = checksum.get_allResponseParams()
    checksum_check = checksum.verify_checksum(recvd_checksum, secret_key, alldata)
    
    response_dict['Checksum Verified?'] = checksum_check
    
    return render(request, 'response.html', {'response_dict':response_dict})


