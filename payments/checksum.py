from hmac import new as hmac
from hashlib import sha256
import binascii

class Checksum:
    def __init__(self, postdata):
        self.postdata = postdata
    
    def get_allParams(self):
        """Concatenates and returns the Name-Value Pairs in the POST data as a single string
        in format name1=value1&name2=value2&.
        """
        # Do not Change params order.
        post_params = [
                        "amount","buyerAddress","buyerCity","buyerCountry","buyerEmail"
                       ,"buyerFirstName","buyerLastName","buyerPhoneNumber","buyerPincode"
                       ,"buyerState","currency","debitorcredit","merchantIdentifier"
                       ,"merchantIpAddress","mode","orderId","product1Description",
                       "product2Description","product3Description","product4Description"
                       ,"productDescription","purpose","returnUrl","shipToAddress","shipToCity"
                       ,"shipToCountry","shipToFirstname","shipToLastname","shipToPhoneNumber"
                       ,"shipToPincode","shipToState","txnDate","txnType","zpPayOption"
                       ]
        
        allParams = ''
        for key in post_params:

            if(key != 'checksum'):
                if(self.postdata[key].find(" ")!=-1) : self.postdata[key] = "".join(self.postdata[key].split())
                if (self.postdata[key] != ""): allParams += key + "=" + self.postdata[key]+"&"

        return allParams
    
    
    def get_allResponseParams(self):
        """Concatenates and returns the Name-Value Pairs in the POST data as a single string
        in format name1=value1&name2=value2&.
        """
        # Do not Change params order.
        response_params = ["orderId","responseCode","responseDescription"]#,"amount","doRedirect"
                            # ,"paymentMode","cardId","cardScheme","cardToken","bank","bankid"
                            # ,"paymentMethod","cardhashid","productDescription","product1Description"
                            # ,"product2Description","product3Description","product4Description","pgTransId","pgTransTime"
                            # ]
        
        allParams_res = ''
        for key in response_params:
            if(key != 'checksum'):
                if(self.postdata[key].find(" ")!=-1) : self.postdata[key] = "".join(self.postdata[key].split())
                if (self.postdata[key] != ""): allParams_res += key + "=" + self.postdata[key]+"&"

        return allParams_res
           
    
    def calculate_checksum(self, secret_key, input_string):
        """ Calculates HMAC SHA256 signature of the data"""
        #byte_key = binascii.unhexlify(secret_key)
        checksum = hmac(secret_key, input_string.encode(), sha256).hexdigest()
        return str(checksum)
    
    def verify_checksum(self, recieved_checksum, secret_key, allParams):
        """Verifies the calculated checksum from response matches with
           checksum given from response
        """ 
        cal_checksum = self.calculate_checksum(secret_key, allParams)
        
        return cal_checksum == recieved_checksum
        
    def output_form(self, checksum):
        """ outputs the data in dict format"""
    
        out = {}
        for key in self.postdata.keys():
            out[key] = self.postdata[key]
        
        out['checksum'] = checksum
        return out
    
    # def output_response(self,checksum_check):
    #     """ If the checksum calculated from zaakpay's response and
    #     checksum in zaakpay's response matches returns output form
    #     of response
    #     """
    #     out = ''
    #     for key in self.postdata.keys():
    #         out[key] = self.postdata[key]
                
    #     out += '<tr><td width="50%" align="center" valign="middle">Checksum Verified ?</td>'
        
    #     if checksum_check:
    #         out += '<td width="50%" align="center" valign="middle">Yes</td></tr>'
    #     else:
    #         out += '<td width="50%" align="center" valign="middle">No</td></tr>'
        
    #     return out
    

        

    
