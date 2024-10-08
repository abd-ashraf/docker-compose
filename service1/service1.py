from flask import Flask, jsonify
import requests
import os
import subprocess
import socket
from requests.exceptions import RequestException

app = Flask(__name__)


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
    return jsonify(combined_info)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8199))
    app.run(host="0.0.0.0", port=port, debug=False)
