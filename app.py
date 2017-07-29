from flask import Flask, render_template
import sys
app = Flask(__name__)

# the root of the site
@app.route("/")
def main():
        return render_template('index.html')

if __name__ == "__main__":
     if sys.argv[1]=="--home":
       app.run()
     else:
        app.run(host='0.0.0.0', port=443, ssl_context=('../healthcraft.crt', '../healthcraft.key'))
