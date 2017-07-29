#!/usr/bin/env python

from CryptoPhotoUtils import CryptoPhotoUtils
import requests

# VERSION: 1.20160609

public_key  = "__PUBLIC_KEY__"   # Get these from https://cryptophoto.com/admin/account
private_key = "__PRIVATE_KEY__"

test_uid    = "123456"    # This is the UserID of your customer. (It does not get revealed)

cp = CryptoPhotoUtils(private_key, public_key, test_uid)  # n.b. CryptoPhotoUtils.py goes in your "site_perl" folder, eg: /usr/lib/perl5/site_perl/

# Adjust this to get the customer's IP address from your web server environment 
r = requests.get("http://curlmyip.com/")
ip = r.text

# The below is for testing in a shell - remove this line if you put this into a web page
r = requests.get("https://cp.vu/show_my_ip")    # Gets your current (external) IP address
ip = r.text

# Request a new CP session 
rv = cp.start_session(ip)
if rv["is_valid"]:
  print 'Session ID: %s \n' % (cp.session_id)    # You need this for calls to CP
else:
  print 'Error: %s\n' % (rv["error"])

rv = cp.get_gen_widget()
if rv["is_valid"]:
  print 'Generate Token Form: %s \n' % (rv["html"])    # This is HTML for your web page to use
else:
  print 'Error: %s\n' % (rv["error"])

# Request a new CP session
rv = cp.start_session(ip, True)

rv = cp.get_auth_widget()
if rv["is_valid"]:
  print 'Auth Token Form: %s\n' % (rv["html"])    # So is this
else:
  print 'Error: %s\n' % (rv["error"])

# Verifies the response to a given challenge
# This is just a demo of how the function should be used;  without valid
# parameters, it is natural that it will return an error message, it is
# supposed to work when integrated with the login, when you provide
# a real, valid IP and valid authentication codes.  
rv = cp.verify_response('selector', 'response_row', 'response_col', 'cp_phc', ip)
if rv["is_valid"]: 
  print 'Authenticated %s \n' % (rv["message"])
else:
  print 'Error: %s\n' % (rv["error"])
