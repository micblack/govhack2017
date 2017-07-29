#!/usr/bin/env python

from CryptoPhotoUtils import CryptoPhotoUtils
import pprint

# VERSION: 1.20131017

server = "http://cryptophoto.com.statw.com"
public_key  = "__PUBLIC_KEY__"   # Get these from https://cryptophoto.com/admin/account
private_key = "__PRIVATE_KEY__"
test_uid    = "123456"    # This is the UserID of your customer. (It does not get revealed)

cp = CryptoPhotoUtils(server, private_key, public_key, test_uid)  # n.b. CryptoPhotoUtils.py goes in your "site_perl" folder, eg: /usr/lib/perl5/site_perl/

POST = {}
POST['cpJWSrfc7515'] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0NDA1MTY0ODIsImZpZWxkc09yZGVyIjoiY3BUVnJlc3BvbnNlLHRlc3RGaWVsZCIsInBpZCI6IjFlMDQwYjlkZjE5NmZlOWE4YjJkZTI5ZDA4NGJiZWYxIiwibmJmIjoxNDQwNTA5MjgyLCJpYXQiOjE0NDA1MTI4ODIsImZpZWxkc1NoYTI1NiI6IjQ2M0ROWmNRUUVaTTFRWHVSaDZTb3RIRnRJOWJoeUVTUVRTaXFZZkdzYjgifQ.Z0Uj_uzGZKqDipaM8jQzjSYwWD6LqnmySRMjfVBGAZ8"
POST['cpTVresponse'] = "--approve--"
POST['testField']    = "1"

res = cp.verify_cptv_response(POST)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(res)
