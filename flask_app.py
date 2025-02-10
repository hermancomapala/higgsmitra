from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import urllib3
import os

app = Flask(__name__)
CORS(app)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Simpan session global
session = requests.Session()

# Dapatkan path absolut ke direktori saat ini
current_dir = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def serve_html():
    return send_from_directory(current_dir, 'index.html')

@app.route('/script.js')
def serve_js():
    return send_from_directory(current_dir, 'script.js')

@app.route('/api/login', methods=['POST'])
def login():
    global session
    url = "https://www.higgsmitra.com/trade/pwdLogin"
    headers = {
        'Host': 'www.higgsmitra.com',
        'Cookie': '_ga=GA1.1.577012423.1737035045; _fbp=fb.1.1737035362448.507048774330132841; _ga_BPWBTPEH1Q=GS1.1.1737035045.1.1.1737036453.3.0.0; trade-cookie-uid=50365; trade-cookie-token=99099119113df897; _ga_3HXQY5733E=GS1.1.1737035045.1.1.1737036681.60.0.0',
        'Content-Length': '106',
        'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Sec-Ch-Ua-Mobile': '?0',
        'Origin': 'https://www.higgsmitra.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.higgsmitra.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': 'u=0, i'
    }
    data = 'v=706172746E657249643D3530333635267077643D6462353634313531653737323733393332656265383066343131613638656366'
    
    session = requests.Session()
    response = session.post(url, headers=headers, data=data, verify=False)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    session.cookies.update(response.cookies)
    
    return jsonify({"status": response.status_code, "data": response.text})

@app.route('/api/check-buyer', methods=['POST'])
def check_buyer():
    global session
    buyer_id = request.json.get('buyerId')
    url = "https://www.higgsmitra.com/trade/queryBuyer"
    headers = {
        'Host': 'www.higgsmitra.com',
        'Content-Length': str(len(f"buyerId={buyer_id}")),
        'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Mobile': '?0',
        'Origin': 'https://www.higgsmitra.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.higgsmitra.com/trade/index?projectId=0',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': 'u=0, i'
    }
    data = f"buyerId={buyer_id}"
    
    response = session.post(url, headers=headers, data=data, verify=False)
    return jsonify({"status": response.status_code, "data": response.text})

@app.route('/api/sell-card', methods=['POST'])
def sell_card():
    global session
    buyer_id = request.json.get('buyerId')
    url = "https://www.higgsmitra.com/trade/sellCard"
    headers = {
        'Host': 'www.higgsmitra.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Mobile': '?0',
        'Origin': 'https://www.higgsmitra.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.higgsmitra.com/trade/index?projectId=0'
    }
    data = f"itemId=6&buyerId={buyer_id}"
    
    response = session.post(url, headers=headers, data=data, verify=False)
    return jsonify({"status": response.status_code, "data": response.text})

# Untuk PythonAnywhere
application = app

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080) 