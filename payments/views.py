from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
from decouple import config

from .checksum import *

secret_key = config('ZAAKPAY_SECRET_KEY') #put your secret key here. Need to be a bytearray
Merchant_ID = config('ZAAKPAY_MERCHENT_KEY')

def payment_page(request):
    return render(request, 'merchant.html')


def posttozaakpay(request):
    postdata = {}
    if request.method == 'POST':
        #postdata = {}
        data = request.POST
        for key in data:
            postdata[key] = data[key]
    
    checksum = Checksum(postdata) # creating Checksum object
    alldata = checksum.get_allParams()
    checksum_value = checksum.calculate_checksum(secret_key, alldata)
    param_dict= checksum.output_form(checksum_value)
    
    # with open(os.getcwd() + '/templates/posttozaakpay.html') as f:
    #     html_template = f.read()
    
    # replacing placeholder in html_template with output_form
    #output = html_template %output_form 
    
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
    #html_template2 = open(os.getcwd() +  '/templates/response.html').read()
    
    # replacing placeholder in html_template with output_form
    # output2 = html_template2 % output_form

    return render(request, 'response.html', {'response_dict':response_dict})


