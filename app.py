from flask import Flask

app = Flask(__name__)

# the root of the site
@app.route("/")
def main():
        return "Welcome!"

    if __name__ == "__main__":
            app.run(host='0.0.0.0', port=443, ssl_context=('../healthcraft.crt', '../hea
            lthcraft.key'))
