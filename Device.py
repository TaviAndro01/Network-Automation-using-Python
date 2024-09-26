from Connection import NetworkSession
import subprocess

class Device:
    def __init__(self, name, ip, username, password, enable_pass):
        # Initializing the device with basic credentials and connection details
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.enable_pass = enable_pass
        self.connection = NetworkSession(ip, username, password)

    def hsrp(self):
        # Configure HSRP
        self.connection.connect(self.enable_pass)

        # User input for HSRP details
        interface = input("Enter the interface ID for HSRP (ex: Gi0/1): ")
        standby_id = input("Enter the standby interface ID (ex: 10): ")
        vrouter_ip = input("Enter the Virtual Router IP address (ex: 192.168.1.1): ")
        priority = input("""For the physical interface priority:
Enter the new priority (1-255) if you want to change it.
Press Enter to keep the default value of 100: """) or "100"

        hsrp_commands = f"""
            int {interface}
            standby version 2
            standby {standby_id} ip {vrouter_ip}
            standby {standby_id} priority {priority}
            standby {standby_id} preempt
            """

        stdout, stderr = self.connection.exec(hsrp_commands)  # Sending HSRP commands to the device

        # Checking for errors and printing success or failure message
        if stderr:
            print(f"Error during HSRP configuration: {stderr}")
        else:
            print("HSRP configuration successful")

        self.connection.close()

    def ping_Device(self):
        # Ping command
        self.connection.connect(self.enable_pass)

        ping_target = input("Ping to: ")  # Input for the target IP to ping

        # Running a ping command to the target IP
        response = subprocess.run(["ping", "-c", "4", ping_target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Checking ping response and printing connectivity results
        if response.returncode == 0:
            print(f"Connectivity test successful. The device at IP {ping_target} is reachable.")
        else:
            print(f"Connectivity test failed. The device at IP {ping_target} could not be reached.")

        self.connection.close()