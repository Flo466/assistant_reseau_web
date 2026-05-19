from flask import Flask, render_template, request
import ipaddress


app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/submit-machine', methods=['POST'])
def submit_machine():
    # Create variables
    hostname = request.form.get('hostname')
    ip_address = request.form.get('ip_address')
    status = request.form.get('status')

    try:
        temperature = float(request.form.get('temperature', 0))
        network_errors = float(request.form.get('network_errors', 0))
    except:
        temperature = 0.0    
        network_errors = 0
    
    alert_message = ""
    
    #IP validation check
    try:
        ipaddress.ip_address(ip_address)
        ip_is_valid = True
    except ValueError:
        ip_is_valid = False

    if not ip_is_valid:
        alert_message = f"Erreur: L'adresse IP '{ip_address}' est invalide !"
        
    elif status == 'Offline':
        alert_message = f"Critique: {hostname} est éteint."
        
    elif temperature > 32.0:
        alert_message = f"Attention: {hostname} a une température trop élevée ({temperature}°C)."
        
    elif network_errors > 3:
        alert_message = f"Attention: Il y a trop d'erreurs réseau ({network_errors})."
        
    else:
        alert_message = f"Système stable pour {hostname}."

    # Pass the variables to the
    return render_template(
        'index.html', 
        hostname=hostname,
        ip_address=ip_address,
        status=status,
        temperature=temperature,
        network_errors=network_errors,
        alert_message=alert_message
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)