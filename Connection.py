import paramiko
from time import sleep


class NetworkSession:

    def __init__(self, ip, username, password):
        # Initialize the session with connection parameters
        self.ip = ip
        self.username = username
        self.password = password
        self.client = None
        self.shell = None

    def connect(self, enable_pass):
        try:
            # Create a new SSH client instance
            self.client = paramiko.SSHClient()

            # Automatically add the host key if it's missing
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the device using provided credentials
            self.client.connect(self.ip, username=self.username, password=self.password)

            # Open a new shell session
            self.shell = self.client.invoke_shell()

            # Send commands to enable privileged mode and enter configuration mode
            self.shell.send(f'en\n{enable_pass}\nconf t\n')

            sleep(1)
        except paramiko.SSHException as e:
            # Print an error message if connection fails and close the session
            print(f"Connectivity test failed {self.ip}: {e}")
            self.close()

    def exec(self, command):
        # Check if there's an active shell session
        if not self.shell:
            print("No active connection. Please establish a connection first.")
            return None, "No active connection."

        # Send the command to the device
        self.shell.send(command + '\n')

        # Read the output from the command
        output = ""
        while self.shell.recv_ready():
            output += self.shell.recv(65535).decode('utf-8')

        return output, ""

    def close(self):
        # Close the SSH client and clean up resources
        if self.client:
            # Send a command to save the configuration
            self.shell.send('\ndo wr\n')

            # Close the client connection
            self.client.close()
            self.client = None
            self.shell = None
