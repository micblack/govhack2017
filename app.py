from flask import Flask, render_template
import sys

# testing: import urllib, hashlib, hmac, time, json, base64

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
testv = app.config['FOO']
print(testv)

# the root of the site
@app.route("/")
def main():
        return render_template('signup.html',test=testv)

@app.route("/test")
def test():
        return render_template('indext.html')

if __name__ == "__main__":
     if len(sys.argv) >1:
         if sys.argv[1]=="--home":
             app.run()
     else:
        app.run(host='0.0.0.0', port=443, ssl_context=('../healthcraft.crt', '../healthcraft.key'))
