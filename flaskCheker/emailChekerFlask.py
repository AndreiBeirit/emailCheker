from flask import Flask, render_template, request, jsonify
import json
import base64
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_verifcode_bnet', methods=['POST'])
def get_verifcode_bnet():
    data = request.get_json()
    url = "https://i/blizzard/getverifcode"
    email = data['email'].strip()
    password = data['password'].replace(' ', '').replace('\t', '')

    if not (len(email.replace(' ', '').replace('\t', '')) > 0 and len(email) <= 40):
        return jsonify({'error': "Email не может быть пустым"})

    elif not (len(password) > 0 and len(password) <= 40):
        return jsonify({'error': "Пароль не может быть пустым"})

    headers = {
        "Authorization": f"Basic {base64.b64encode('imap-user:Ltylhfhbev123~'.encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
    }

    payload = {'Email': email, 'Password': password}

    response = requests.post(url, headers=headers, data=payload)
    response_error = json.loads(response.text)
    error_value = response_error['response']

    if response.status_code == 200:
        pass
    else:
        return jsonify({'error': error_value})
    
    try:
        response_data = json.loads(response.text)
        code_value = response_data['code']
        return jsonify({'code': code_value})
    except KeyError:
        return jsonify({'error': 'Ошибка при получении кода разблокировки'})

if __name__ == '__main__':
    app.run(debug=True)
