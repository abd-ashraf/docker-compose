from flask import Flask, jsonify, request
import requests
import os
import subprocess
from requests.exceptions import RequestException
import time
import threading
from datetime import datetime

app = Flask(__name__)

current_state = "INIT"
state_transitions = []

@app.route("/state", methods=["GET"])
def get_state():
    return current_state, 200, {'Content-Type': 'text/plain'}

def log_state_transition(old_state, new_state):
   timestamp = datetime.now().strftime("%Y-%m-%dT%H.%M:%S.%fZ")
   state_transitions.append(f"{timestamp}: {old_state}->{new_state}")

@app.route("/run-log", methods=["GET"])
def get_run_log():
   return "\n".join(state_transitions), 200, {'Content-Type': 'text/plain'}

@app.route("/state", methods=["PUT"])
def set_state():
   global current_state
   new_state = request.get_data().decode('utf-8').strip()
   
   if new_state not in ["INIT", "RUNNING", "PAUSED", "SHUTDOWN"]:
       return "Invalid state", 400
   
   if new_state != current_state:
       log_state_transition(current_state, new_state)
       current_state = new_state
       
   return "OK", 200

def check_state():
    """Check if service should respond based on current state"""
    if current_state == "PAUSED":
        return jsonify({"error": "Service is paused"}), 503
    # elif current_state == "INIT":
    #     return jsonify({"error": "Service needs login"}), 401
    # elif current_state == "SHUTDOWN":
    #     return jsonify({"error": "Service is shutting down"}), 503
    return None

def get_system_info():
    try:
        # Get IP address
        ip_address = subprocess.check_output(
            "hostname -i", shell=True).decode().strip()

        # Get running processes
        running_processes = subprocess.check_output(
            "ps -ax", shell=True).decode().strip()

        # Get disk space
        disk_space = subprocess.check_output(
            "df -h /", shell=True).decode().strip()

        # Get uptime
        uptime = subprocess.check_output(
            "uptime -p", shell=True).decode().strip()

        return {
            "IP Address": ip_address,
            "Running Processes": running_processes,
            "Disk Space": disk_space,
            "Uptime": uptime,
        }
    except Exception as e:
        return {"error": f"Failed to retrieve system information: {str(e)}"}


@app.route("/", methods=["GET"])
def home():
    # Check state before processing
    state_check = check_state()
    if state_check:
        return state_check
    
    service1_info = get_system_info()

    try:
        service2_response = requests.get(
            "http://service2:5000/system_info", timeout=5)
        service2_response.raise_for_status()
        service2_info = service2_response.json()
    except RequestException as e:
        service2_info = {
            "error": f"Service2 is not available. Error: {str(e)}"}

    combined_info = {"Service1": service1_info, "Service2": service2_info}

    time.sleep(2)

    return jsonify(combined_info)


@app.route("/stop", methods=["POST"])
def stop_services():
    def shutdown():
        time.sleep(0.1)  # Small delay to ensure response is sent
        try:
            # Stop service2 first
            try:
                requests.post('http://service2:5000/stop', timeout=1)
            except:
                pass  # Service2 might already be stopping

            # Stop other service1 instances
            other_services = ['service1-1:8199',
                              'service1-2:8199', 'service1-3:8199']
            for service in other_services:
                try:
                    requests.post(f'http://{service}/stop', timeout=1)
                except:
                    pass  # Services might already be stopping

            time.sleep(0.1)  # Small delay before exit
            os._exit(0)
        except:
            os._exit(1)

    # Start shutdown in a separate thread
    threading.Thread(target=shutdown).start()

    return jsonify({"message": "Stopping services..."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8199))
    app.run(host="0.0.0.0", port=port, debug=False)
