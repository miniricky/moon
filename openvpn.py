import subprocess
import time
import os

# Function to start the VPN connection
def connect_vpn(vpn_config_file, auth_file):
    try:
        # Run OpenVPN with the config file and authentication file
        process = subprocess.Popen(
            ['C:/Program Files/OpenVPN/bin/openvpn.exe', '--config', vpn_config_file, '--auth-user-pass', auth_file, '--disable-dco'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # This will treat the output as text instead of bytes
        )
        
        print("Attempting to connect to VPN...")
        
        # Read and print stdout and stderr line by line in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"OUTPUT: {output.strip()}")
                
            # Check for successful connection message
            if "Initialization Sequence Completed" in output:
                print("VPN connection established successfully.")
                return process  # Exit the function and return the process

    except subprocess.TimeoutExpired:
        print("Timeout expired while connecting to VPN.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

# Function to disconnect from the VPN
def disconnect_vpn(process):
    if process:
        process.terminate()
        process.wait()
        print("VPN disconnected.")