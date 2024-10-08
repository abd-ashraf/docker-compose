from flask import Flask, jsonify
import requests
import os
import psutil
import socket
from requests.exceptions import RequestException
import time

app = Flask(__name__)


def get_running_processes():
    process_info_list = []
    for proc in psutil.process_iter(["pid", "name", "username", "status"]):
        try:
            # Append detailed information for each process
            process_info_list.append(
                f"PID: {proc.info['pid']}, Name: {proc.info['name']}, "
                f"User: {proc.info['username']}, Status: {proc.info['status']}"
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Skip processes that are not accessible

    # Combine all process details into a single string for easier display
    return "\n".join(process_info_list)


# Helper function to get the system uptime in hours
def format_uptime():
    boot_time_seconds = (
        psutil.boot_time()
    )  # Get the system boot time in seconds since epoch
    current_time_seconds = time.time()  # Get the current time in seconds since epoch
    uptime_seconds = (
        current_time_seconds - boot_time_seconds
    )  # Calculate uptime in seconds
    uptime_hours = uptime_seconds / 3600  # Convert seconds to hours
    return f"{uptime_hours:.2f} hours"  # Format uptime in hours


def get_system_info():
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
        running_processes = get_running_processes()
        disk_usage = psutil.disk_usage("/")
        disk_space = f"Total: {disk_usage.total / (1024**3):.2f}GB, Used: {disk_usage.used / (1024**3):.2f}GB, Free: {disk_usage.free / (1024**3):.2f}GB"
        uptime = format_uptime()

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
        service2_response = requests.get("http://service2:5000/system_info", timeout=5)
        service2_response.raise_for_status()
        service2_info = service2_response.json()
    except RequestException as e:
        service2_info = {"error": f"Service2 is not available. Error: {str(e)}"}

    combined_info = {"Service1": service1_info, "Service2": service2_info}
    return jsonify(combined_info)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8199))
    app.run(host="0.0.0.0", port=port, debug=False)
