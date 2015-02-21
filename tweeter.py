from flask import *
import json

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def primary():
    if request.method == "GET":
        return "I'm alive."
    elif request.method == "POST":
        data = json.loads(request.data)
        print data
        print data['hook']['config']['secret']
        print "New commit by %s, %s" % (str(data['commits'][0]['author']['username']), str(data['commits'][0]['message']))
        return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10060, debug="true")
