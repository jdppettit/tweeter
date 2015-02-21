from flask import *
from config import *
from hashlib import sha1

import json
import hmac

app = Flask(__name__)

def verify_secret(request, data):
    sha, signature = request.headers.get('X-Hub-Signature').split('=')
    if sha != 'sha1':
        abort(403)
    res = hmac.new(secret, msg=data, digestmod=sha1)
    if not hmac.compare_digest(res.hexdigest(), signature):
        return(403)

@app.route('/', methods=['GET','POST'])
def primary():
    if request.method == "GET":
        return "I'm alive."
    elif request.method == "POST":
        data = json.loads(request.data)
        verify_secret(request, data)
        print "New commit by %s, %s" % (str(data['commits'][0]['author']['username']), str(data['commits'][0]['message']))
        return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10060, debug="true")
