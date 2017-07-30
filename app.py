# This is the HealthCraft Govhack2017 entry from high-fliers team.

from flask import Flask, render_template
import sys
from CryptoPhotoUtils import CryptoPhotoUtils

import urllib, hashlib, hmac, time, json, base64	# CryptoPhoto dependencies

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
testv = app.config['FOO']
private_key = app.config['CP_PUBLICKEY']
public_key = app.config['CP_PRIVATEKEY']

test_uid    = "123456"    # This is the UserID of your customer. (It does not get revealed)

#cp = CryptoPhotoUtils(private_key, public_key, test_uid)

# the root of the site
@app.route("/")
def main():
        return render_template('index.html',test=testv)

@app.route("/signup")
def signup():
        return render_template('signup.html')

@app.route("/main")
def signup():
        return render_template('main.html')

if __name__ == "__main__":
     if len(sys.argv) >1:
         if sys.argv[1]=="--home":
             app.run()
     else:
        app.run(host='0.0.0.0', port=443, ssl_context=('../healthcraft.crt', '../healthcraft.key'))
