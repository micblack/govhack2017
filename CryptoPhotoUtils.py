"""
  This is a Python library that handles calling CryptoPhoto API.
     - Main Page
         http://cryptophoto.com/
     - About Cryptophoto
         http://cryptophoto.com/about
     - Register to CryptoPhoto
         http://cryptophoto.com/demo/register/
 
  Copyright(c) 2016 CryptoPhoto -- http://cryptophoto.com/
  AUTHORS: CryptoPhoto
 
  VERSION: 1.20160609
 
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:
 
  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.
 
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
"""

import urllib2, urllib, hashlib, hmac, time, json, base64

class CryptoPhotoUtils(object):
  """Class containing all operations with the CryptoPhoto service."""

  def __init__(self, server, privatekey, publickey, uid):
    self.server      = server if server else "https://cryptophoto.com"
    self.private_key = privatekey
    self.public_key  = publickey
    self.user_id     = uid
    self.session_id  = None
    self.secure      = True
    self.user_agent  = 'CryptoPhoto Python'
    if self.secure:
      self.protocol = 'https'
  
  def __post_request(self, url, value_dict):
    """Sends key/value pairs in value_dict to the specified url in form-style
    encoding via HTTP POST"""
    for k, v in value_dict.iteritems():
      value_dict[k] = self.__tryEncode(v)
      
    params = urllib.urlencode(value_dict)

    request = urllib2.Request(
      url = url,
      data = params,
      headers = {
        'Content-type' : 'application/x-www-form-urlencoded',
        'User-agent'   : self.user_agent
      }
    )
    try:
      httpresp = urllib2.urlopen(request)
    except:
      return False

    ret = httpresp.read()
    httpresp.close()
    return ret

  def start_session(self, ip, authentication = False):
    """Method for fetching valid session ids from the corresponding
    CryptoPhoto service."""
    ret = {}
    
    t = int(time.time())
    
    response = self.__post_request('%s/api/get/session' % (self.server), {
      'publickey' : self.public_key,
      'uid'       : self.user_id,
      'time'      : t,
      'signature' : self.make_signature(self.user_id, self.public_key, self.private_key, t),
      'ip'        : ip,
      'authentication': "true" if authentication else "false"
    })

    if not response:
      ret["is_valid"] = False
      ret["error"] = "Service-unavailable"
      return ret
    
    return_values = response.splitlines()
 
    print return_values
    print '\n'
   
    try:
      if return_values[0] == 'success':
        ret["is_valid"] = True
        ret["sid"] = return_values[1]
        self.session_id = return_values[1]
        self.session_id_used = False
        if return_values[2] == 'true':
          ret["has_token"] = True
      else:
        ret["is_valid"] = False
        ret["error"] = return_values[1]
        if not return_values[3]:
          ret["errip"] = ''
        else:
          ret["errip"] = return_values[3]
    except:
      ret["is_valid"] = False
      ret["error"] = 'Malformed-response'

    return ret

  def get_auth_widget(self):
    """Fetches a CryptoPhoto authentification widget."""
    ret = {}
    if self.session_id:
      ret["html"] = ('<script type=\"text/javascript\" src=\"%s/api/challenge'
          '?sd=%s\"></script>' % (self.server, self.session_id))
      ret["is_valid"] = True
    else:
      ret["is_valid"] = False
      ret["error"] = 'invalid-session-id'
    return ret

  def get_gen_widget(self):
    """Fetches a CryptoPhoto token generation widget."""
    ret = {}
    if self.session_id:
      ret["html"] = ('<script type=\"text/javascript\" src=\"%s/api/token?sd='
          '%s\"></script>' % (self.server, self.session_id))
      ret["is_valid"] = True
    else:
      ret["is_valid"] = False
      ret["error"] = 'invalid-session-id'
    return ret

  def verify_response(self, selector, response_row, response_col, cp_phc, ip):
    """Verifies a response for a previously sent CryptoPhoto challenge."""
    ret = {}
    
    if selector is None:
      ret["is_valid"] = False;
      ret["error"] = "Selector is not defined";
      return ret
    else :
      if (response_row is None or response_col is None) and cp_phc is None:
        ret["is_valid"] = False;
        ret["error"] = "Post data invalid";
        return ret

    t = int(time.time())
    
    response = self.__post_request('%s/api/verify' % (self.server), {
      'publickey'    : self.public_key,
      'uid'          : self.user_id,
      'response_row' : response_row,
      'response_col' : response_col,
      'selector'     : selector,
      'cph'          : cp_phc,
      'ip'           : ip,
      'signature'    : self.make_signature(self.user_id, self.public_key, self.private_key, t),
      'time'         : t
    })
    
    if not response:
      ret["is_valid"] = False
      ret["error"] = "service-unavailable"
      return ret  

    return_values = response.splitlines()

    ret["is_valid"] = False

    try:
      m = return_values[1]
      if return_values[0] == 'success':
        ret["is_valid"] = True
        ret["message"]  = m
      else:
        ret["error"] = m
    except:
      ret["is_valid"] = False
      ret["error"] = 'malformed-response'
      
    return ret

  def verify_cptv_response(self, parms):
    """Verifies a response for a previously sent CryptoPhoto transaction verification."""
    ret = {}

    if not parms['cpJWSrfc7515']:
      ret["is_valid"] = False
      ret["error"] = "JWT token not provided"

    response = self.__post_request('%s/api/verify/cptv.json' % (self.server), {
      'token': parms['cpJWSrfc7515']
    })

    if not response:
      ret["is_valid"] = False
      ret["error"] = "service-unavailable"
      return ret

    answer = json.loads(response)

    if answer and 'success' in answer:
      token = parms['cpJWSrfc7515']
      splits = token.split(".")

      missing_padding = 4 - len(splits[1]) % 4
      if missing_padding:
        splits[1] += b'='* missing_padding

      claim = json.loads(base64.urlsafe_b64decode(splits[1]))

      if claim and 'fieldsOrder' in claim and 'fieldsSha256' in claim:
        fieldsOrder  = claim['fieldsOrder'];
        fieldsSha256 = claim['fieldsSha256'];

        fields = fieldsOrder.split(",")

        shacontent = ""

        for field in fields:
          if parms[field]:
            shacontent += parms[field]

        m = hashlib.sha256()
        m.update(shacontent)

        shacontent = base64.urlsafe_b64encode(m.digest());

        shacontent = shacontent.replace("=","")
        fieldsSha256 = fieldsSha256.replace("=","")

        if fieldsSha256 == shacontent:
          ret["is_valid"] = True
          return ret
        else:
          ret["is_valid"] = False
          ret["error"] = "POST/GET fields values have been changed"
          return ret


    else:
      ret["is_valid"] = False
      ret["error"] = answer['description']
      return ret

  def make_signature(self, uid, publickey, privatekey, time):
    return hmac.new(privatekey, privatekey + str(time) + uid + publickey, hashlib.sha1).hexdigest()

  def __tryEncode(self, s):
    if isinstance(s, unicode):
      return s.encode('utf-8')
    return s
  

