from flask import *
from config import *
from hashlib import sha1

import requests
import json
import hmac

app = Flask(__name__)

def verify_secret(request, data):
    sha, signature = request.headers.get('X-Hub-Signature').split('=')
    if sha != 'sha1':
        abort(403)
    res = hmac.new(secret, msg=data, digestmod=sha1)
    if res.hexdigest() != signature:
        return(403)

def shorten(url):
    response = requests.post('https://ptpb.pw/u', data={'c':url})
    shortened_url = response.headers.get('Location')
    return shortened_url

@app.route('/', methods=['GET','POST'])
def primary():
    if request.method == "GET":
        return "I'm alive."
    elif request.method == "POST":
        verify_secret(request, request.data)

        data = json.loads(request.data)

        commit_message = str(data['head_commit']['message'])
        commit_user = str(data['head_commit']['author']['username'])
        commit_url = str(data['head_commit']['url'])
        repo_name = str(data['repository']['name'])
        
        shortened_url = shorten(commit_url)

        message = "New commit by %s on %s: %s %s" % (commit_user,
                                                        repo_name,
                                                        commit_message,
                                                        shortened_url)
        if len(message) > 255:
            delta = len(message) - 255
            delta = delta + 3
            temp_commit_message = str(data['commits'][0]['message'])[:delta]
            temp_commit_message += "..."
            commit_message = temp_commit_message

        message = "New commit by %s on %s: %s %s" % (commit_user,
                                                        repo_name,
                                                        commit_message,
                                                        shortened_url)

        print message

        return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10060, debug="true")
