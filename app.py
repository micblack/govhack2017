# This is the HealthCraft Govhack2017 entry from high-fliers team.

from flask import Flask, render_template, request
import sys
from CryptoPhotoUtils import CryptoPhotoUtils

import urllib, hashlib, hmac, time, json, base64	# CryptoPhoto dependencies
import requests

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
testv = app.config['FOO']
private_key = app.config['CP_PUBLICKEY']
public_key = app.config['CP_PRIVATEKEY']

test_uid    = "123456"    # This is the UserID of your customer. (It does not get revealed)
server = "https://cryptophoto.com"
cp = CryptoPhotoUtils(server, private_key, public_key, test_uid)

# the root of the site
@app.route("/")
def index():
        return render_template('index.html',test=testv)

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        return do_the_signup()
    else:
        return render_template('signup.html')

def do_the_signup():



        # Adjust this to get the customer's IP address from your web server environment 
        #r = request.remote_addr requests.get("http://curlmyip.com/")
        ip = request.remote_addr    #r.text

        print 'ip is %s\n' % (ip)

        # Request a new CP session 
        rv = cp.start_session(ip)
        if rv["is_valid"]:
          print 'Session ID: %s \n' % (cp.session_id)    # You need this for calls to CP
        else:
          print 'Error1: %s\n' % (rv["error"])

        rv = cp.get_gen_widget()
        if rv["is_valid"]:
          print 'Generate Token Form: %s \n' % (rv["html"])    # This is HTML for your web page to use
        else:
          print 'Error2: %s\n' % (rv["error"])

        # Request a new CP session
        rv = cp.start_session(ip, True)

        rv = cp.get_auth_widget()
        if rv["is_valid"]:
          print 'Auth Token Form: %s\n' % (rv["html"])    # So is this
        else:
          print 'Error3: %s\n' % (rv["error"])

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

        return render_template('hello.html',test=testv)
        
@app.route("/main")
def main():
        return render_template('main.html')

if __name__ == "__main__":
     if len(sys.argv) >1:
         if sys.argv[1]=="--home":
             app.run()
     else:
        app.run(host='0.0.0.0', port=443, ssl_context=('../healthcraft.crt', '../healthcraft.key'))


