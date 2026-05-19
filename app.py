from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/submit-machine', methods=['POST'])
def submit_machine():
    machine_data = {
        "hostname": request.form.get('hostname'),
        "ip_address": request.form.get('ip_address'),
        "status": request.form.get('status'),
        "temperature": request.form.get('temperature'),
        "network_errors": request.form.get('network_errors')
    }
    return render_template('index.html', data=machine_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)