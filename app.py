# This is the HealthCraft Govhack2017 entry from high-fliers team.

from flask import Flask, render_template, request
import sys
from CryptoPhotoUtils import CryptoPhotoUtils

import urllib, hashlib, hmac, time, json, base64	# CryptoPhoto dependencies
import requests

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
testv = app.config['FOO']
privatekey = app.config['CP_PUBLICKEY']
publickey = app.config['CP_PRIVATEKEY']
salt = app.config['CP_SALT']


test_uid    = "12345"    # This is the UserID of your customer. (It does not get revealed)
server = "https://cryptophoto.com"
cp = CryptoPhotoUtils(server, privatekey, publickey, test_uid)

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
        
@app.route("/account")
def account():
        
        ip = request.remote_addr    #r.text
        
        res = get_api_session(test_uid,ip)
        
        display = ''
        error = ''
        sid = ''
        
        if res['is_valid']:
          sid = res['sid']
        else:
          error = res['error']
          if 'errdesc' is res:
            error += res['errdesc']
        
        if sid:
          display = ("<div id='cp_widget'>Loading...</div>"
                     "<script type='text/javascript'"
                     "src='https://cryptophoto.com/api/token?sd=" + sid + "'>"
                     "</script>")
        elif error:
          display = "<div>Error: " + error + "</div>"
        
        out = '''<html>
        <head>
        <meta charset="UTF-8">
        <title>User Account</title>
        </head>
        <body>
          <h2>Manage Your Token</h2>
          {display}
        </body>
        </html>'''
        
        out = out.format(display=display)

        print 'out=%s\n' % (out)

        return out # render_template('account.html',content = out)



@app.route("/main")
def main():
        return render_template('main.html')



def get_api_session(uid, ip, authentication = False):
  uid = hashlib.sha1(uid + salt).hexdigest()
  t = int(time.time())
  sign = hmac.new(privatekey, privatekey + str(t) + uid + publickey, hashlib.sha1).hexdigest()

  postdata = {
    'publickey' : publickey,
    'uid'       : uid,
    'time'      : t,
    'signature' : sign,
    'ip'        : ip
  }

  if authentication:
    postdata["authentication"] = "true"

  response = urllib.urlopen("https://cryptophoto.com/api/get/session", urllib.urlencode(postdata))

  ret = {}

  if not response:
    ret["is_valid"] = False
    ret["error"] = "service-unavailable"
    return ret

  return_values = response.read().splitlines()

  try:
    if return_values[0] == 'success':
      ret["is_valid"] = True
      ret["sid"] = return_values[1]
      ret["has_token"] = True if return_values[2] == 'true' else False
    else:
      ret["is_valid"] = False
      ret["error"] = return_values[1]
      ret["errip"] = return_values[3] if len(return_values) == 4 else ''

  except:
    ret["is_valid"] = False
    ret["error"] = 'malformed-response'

  return ret

def verify_cptv_response(POST):
  ret = {}
 
  if 'cpJWSrfc7515' not in POST:
    ret["is_valid"] = False
    ret["error"] = 'JWT token not provided'
    return ret
   
  postdata = {
    'token': POST['cpJWSrfc7515']
  }

  response = urllib.urlopen("https://cryptophoto.com/api/verify/cptv.json", urllib.urlencode(postdata))

  if not response:
    ret["is_valid"] = False
    ret["error"] = "service-unavailable"
    return ret

  return_value = response.read()

  try:
    obj = json.loads(return_value)
  except:
    ret["is_valid"] = False
    ret["error"] = "CRYPTOPHOTO responded with invalid format"
    return ret
   
  if 'success' not in obj or not obj['success']:
    ret["is_valid"] = False
    ret["error"] = obj['description']
    return ret
 
  jwt = POST['cpJWSrfc7515'];
  tks = string.split(jwt, '.');
  payload = json.loads(base64.urlsafe_b64decode(tks[1]))
 
  if not payload or 'fieldsOrder' not in payload or 'fieldsSha256' not in payload:
    ret["is_valid"] = False
    ret["error"] = 'JWT payload missing fields'
    return ret
 
  fields = string.split(payload['fieldsOrder'], ',')
  shacontent = ''
 
  for field in fields:
    if field in POST and POST[field]:
      shacontent += POST[field]
   
  shacontent = base64.b64encode(hashlib.sha256(shacontent).digest())
 
  fieldsSha256 = payload['fieldsSha256']
  fieldsSha256 = fieldsSha256.rstrip('=')
  shacontent = shacontent.rstrip('=')
 
  if fieldsSha256 == shacontent:
    ret["is_valid"] = True
  else:
    ret["is_valid"] = False
    ret["error"] = 'POSTed field values have been changed'
   
  return ret




# Do not change below

if __name__ == "__main__":
     if len(sys.argv) >1:
         if sys.argv[1]=="--home":
             app.run()
     else:
        app.run(host='0.0.0.0', port=443, ssl_context=('../healthcraft.crt', '../healthcraft.key'))
















