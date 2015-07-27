# -*- coding: utf-8 -*-

from django.conf import settings
import simplejson
import requests

if __name__ == "__main__":
    print "===================== WEBSERVICE TEST ======================="
    
    try:
        email = "client@email.com"
        passw = "client"
        url = "http://chemiresto.local:8000/webservice/accounts/update/my_account/"
        
        headers = {
            "Authorization":"Basic %s" % ( ":".join([email, passw]).encode('Base64').replace('\n','') ),
        }
        
        data = {
            
        }
        
        r = requests.post(url, 
                          headers=headers,
                          data={'data':"%s" % ( simplejson.dumps(data).encode('Base64').replace('\n','') )})
        
        print r.text
        
    except Exception as e:
        print str(e)
    
    # END OF webservice_test