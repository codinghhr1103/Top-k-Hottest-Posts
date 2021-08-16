from flask import Flask, redirect, url_for, request
import json

app = Flask(__name__)

@app.route('/daily')
def report_daily():
    # fetch parameters from the config file into BoardConfigs
    with open("/home/laphy/Top_K_Hottest/daily_result.json", "r") as f:
        ret = json.load(f)
    return ret

@app.route('/frequent')
def report_frequently():
    # fetch parameters from the config file into BoardConfigs
    with open("/home/laphy/Top_K_Hottest/frequent_result.json", "r") as f:
        ret = json.load(f)
    return ret

@app.route('/register',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        password = int(request.form['password'])
        if password != 230716134:
            return "password is incorrect"

        with open("config.json", "r") as f:
            config = json.load(f)

        with open("CommonCase.json", "r") as f:
            CommonCase = json.load(f)

        Email = str(request.form['Email'])
        URL = str(request.form['URL'])

        TopK = request.form['TopK']
        if TopK == '' or TopK.isnumeric() == False:
            TopK = CommonCase['TopK']
        else:
            TopK = int(TopK)
            if TopK <1 or TopK>10:
                TopK = CommonCase['TopK']

        ReplyCntPerInterval = request.form['ReplyCntPerInterval']
        if ReplyCntPerInterval == '' or ReplyCntPerInterval.isnumeric() == False:
            ReplyCntPerInterval = CommonCase['ReplyCntPerInterval']
        else:
            ReplyCntPerInterval = int(ReplyCntPerInterval)
            if ReplyCntPerInterval < 1:
                ReplyCntPerInterval = CommonCase['ReplyCntPerInterval']

        #the config is a dict, but we need to make sure config[Email] exists as a dict, and then make sure config[Email][URL] exists as a dict
        if Email not in config.keys():
            config[Email] = dict()
        if URL not in config[Email].keys():
            config[Email][URL] = dict()

        config[Email][URL]['TopK'] = TopK
        config[Email][URL]['ReplyCntPerInterval'] = ReplyCntPerInterval

        with open("config.json", "w", encoding='utf-8') as o:
            json.dump(config, o)

        return "success"
    else:
        with open("registration.html", "r") as f:
            html = f.read()
        return html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
