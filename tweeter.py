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
        return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10060, debug="true")
