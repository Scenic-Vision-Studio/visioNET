from flask import Flask, render_template, request, jsonify, redirect, url_for
import random

# Colori per syslog
VERDE = '\033[92m'
GIALLO = '\033[93m'
ROSSO = '\033[91m'
ENDC = '\033[0m'

app = Flask(__name__)
NET_code = random.randint(10000, 99999)
print(f'{GIALLO}The unique NET_code for this session is {NET_code}.{ENDC}')

@app.route('/', methods=['GET', 'POST'])
def index():
    global NET_code
    cookie = request.cookies.get('last-code')
    if cookie is not None and int(cookie) == NET_code:
        return redirect(url_for('chat'))

    if request.method == 'POST':
        username = request.form.get('user')
        user_net_code = request.form.get('net-code')

        if int(user_net_code) == NET_code:
            print(f'{VERDE}{username} code OK {ENDC}- connecting...')
            resp = redirect(url_for('chat'))
            resp.set_cookie('last-code', user_net_code)
            resp.set_cookie('username', username)
            return resp

    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    global NET_code
    cookie = request.cookies.get('last-code')
    username = request.cookies.get('username')
    if cookie is None or int(cookie) != NET_code:
        return redirect(url_for('index'))
    
    return render_template('chat.html', username=username)

@app.route('/api/v1/resources/chat', methods=['GET'])
def api():
    return jsonify()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')