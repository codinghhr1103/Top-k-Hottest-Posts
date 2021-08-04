from flask import Flask
import json

app = Flask(__name__)
@app.route('/')
def report_daily():
    # fetch parameters from the config file into BoardConfigs
    with open("/home/laphy/Top_K_Hottest/daily_result.json", "r") as f:
        ret = json.load(f)
    return ret

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
