import subprocess
import time

# Function to start the VPN connection
def connect_vpn(vpn_config_file, auth_file, max_attempts=3):
    attempt_count = 0

    while attempt_count < max_attempts:
        try:
            # Run OpenVPN with the config file and authentication file
            print(f"Attempting to connect to VPN... (Attempt {attempt_count + 1}/{max_attempts})")
            process = subprocess.Popen(
                ['C:/Program Files/OpenVPN/bin/openvpn.exe', '--config', vpn_config_file, '--auth-user-pass', auth_file, '--disable-dco'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # This will treat the output as text instead of bytes
            )
            
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
                
                # Check for authentication failure
                if "AUTH_FAILED" in output or "AUTH_FAILURE" in output:
                    print("VPN authentication failed. Trying again...")
                    process.terminate()  # Terminate the current process
                    break  # Break the inner while loop to try again
                
            attempt_count += 1
            time.sleep(3)  # Wait a few seconds before trying again

        except subprocess.TimeoutExpired:
            print("Timeout expired while connecting to VPN.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    # If all attempts fail, return None
    print("Max attempts reached. Could not connect to VPN.")
    return None

# Function to disconnect from the VPN
def disconnect_vpn(process):
    if process:
        process.terminate()
        process.wait()
        print("VPN disconnected.")