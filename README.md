# GovHack 2017 Project: The Health Craft by High Flyers

The project aims to deliver healthcare outcomes for those with difficulty to travel to receive health care, e.g. in-home patients with no access to suitable public transport, irregular or expensive personal transportation options, or medical unsuitability to move beyond the home.

This is a project using open government data for the GovHack 2017 hackathon.

View the video here: https://drive.google.com/file/d/0B8cD4u2-uC6EZGRuNEFQczRpbXc/view

Experience the web site here: https://healthcraft.team.sh/account

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

**There is no build system, just work from the static folder for views**

### Pre-install instructions (if running locally)

This project requires Python@2.7
```
sudo pip install flask
```

It will also require a config.cfg file in the root to run locally
```
DEBUG = True
DEVELOPMENT = True
CP_PUBLICKEY  = 'yourkey'
CP_PRIVATEKEY = 'yourkey'
CP_SALT = 'yourkey'
```

### Run on server

```
sudo python app.py
```

### Run on your local machine:

```
python app.py --home
```

## Built With

* [CryptoPhoto](https://cryptophoto.com/) - The 2FA service
* [ElementUI](http://element.eleme.io/) - UI framework
* [VueJS](https://vuejs.org/) - Front end framework
* Django, Flask, Python

* CryptoPhoto python dependencies: urtlllb, hashlib, hmac, time, json, base64  

## Contributing

Given that this is really a holding place for a one time weekend hackathon, we're not expecting contributions from outside of our team or after the weekend.

## Versioning

None. Whatever is here is it.

## Authors

* **Dan Bryar**
* **Chris Drake** - [CryptoPhoto](https://cryptophoto.com/)
* **Ric Pruss**
* **Mic Black** - [Mic's Lab](https://micslab.com/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* GovHack 2017 Sunshine Coast crew
