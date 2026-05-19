from flask import Flask, render_template, request
import ipaddress

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-machine', methods=['POST'])
def submit_machine():
    # Extract in variables
    hostname = request.form.get('hostname')
    ip_address = request.form.get('ip_address')
    status = request.form.get('status')

    # 2. Conversion
    def safe_float(value, default):
        try:
            if value is None or value == "":
                return default
            return float(value)
        except (ValueError, TypeError):
            return default

    temperature = safe_float(request.form.get('temperature'), 0.0)
    network_errors = safe_float(request.form.get('network_errors'), 0.0)
    cpu_usage = safe_float(request.form.get('cpu_usage'), 0.0)
    disk_space = safe_float(request.form.get('disk_space'), 100.0)
    
    # 3. Check if IP is valid
    try:
        ipaddress.ip_address(ip_address)
        ip_is_valid = True
    except ValueError:
        ip_is_valid = False

    # 4. Logic
    alerts = []
    
    # Check IP
    if not ip_is_valid:
        alerts.append(f"Erreur: L'adresse IP '{ip_address}' est invalide !")
        
    # Check Statut
    if status == 'Offline':
        alerts.append(f"Critique: {hostname} est éteint.")
        
    # Check Température
    if temperature > 32.0:
        alerts.append(f"Attention: {hostname} a une température trop élevée ({temperature}°C).")
        
    # Check Erreurs Réseau
    if network_errors > 3:
        alerts.append(f"Attention: Il y a trop d'erreurs réseau ({network_errors}).")
        
    # Check CPU
    if cpu_usage > 90.0:
        alerts.append(f"Danger: Le CPU de {hostname} est trop élevé ({cpu_usage}%).")
        
    # Check Disque
    if disk_space < 10.0:
        alerts.append(f"Critique: L'espace disque sur {hostname} est faible ({disk_space}% restant).")
        
    # Si aucune alerte n'a été levée
    if not alerts:
        alerts.append(f"Système stable pour {hostname}.")

    # 5. Send var to HTML
    return render_template(
        'index.html', 
        hostname=hostname,
        ip_address=ip_address,
        status=status,
        temperature=temperature,
        network_errors=network_errors,
        cpu_usage=cpu_usage,
        disk_space=disk_space,
        alert_messages=alerts 
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)