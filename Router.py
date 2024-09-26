from Device import Device  # Importing the base class 'Device' for basic device functionality


class Router(Device):  # Inheriting from 'Device'
    def rip(self):
        # Configure RIP
        self.connection.connect(self.enable_pass)

        networks = []  # List to store the networks to be added to RIP
        while True:
            # User input to add networks for RIP configuration
            network = input("Enter the IP address of a network to add (ex: 192.168.1.0) or press Enter to finish: ")
            if network:
                networks.append(network)


            else:
                break  # Exiting loop when no input is provided

        # User input to decide whether to redistribute static routes into RIP
        redistribute_input = input("Do you want to redistribute static routes from this device? (yes/no): ").lower()
        if redistribute_input == 'yes':
            redistribute_command = "redistribute static"
        elif redistribute_input == 'no':
            redistribute_command = ""
            print("Static routes will not be redistributed.")
        else:
            redistribute_command = ""
            print("Invalid option entered. Static routes will not be redistributed.")

        rip_commands = f"""
                router rip
                version 2
                no auto-summary
                {redistribute_command}
            """
        for network in networks:  # Adding each network to the RIP configuration
            rip_commands += f"network {network}\n"

        # Executing the RIP configuration commands
        stdout, stderr = self.connection.exec(rip_commands)

        # Checking for errors and printing success or failure messages
        if stderr:
            print(f"Error configuring RIP: {stderr}")
        else:
            print("RIP configuration successful")

        self.connection.close()  # Closing the SSH connection

    def dhcp(self, ip):
        # Configure DHCP
        self.connection.connect(self.enable_pass)

        # Breaking down the IP to create a base network IP
        network_ip = '.'.join(ip.split('.')[:3])

        # Gathering input for DHCP configuration
        lan_id = input("Enter the LAN ID(ex: 10): ")
        network = input("Enter the IP address of the DHCP pool(ex: 192.168.1.0): ")
        subnet_mask = input("Enter the subnet mask(ex: 255.255.255.0): ")
        n_switch = int(input("Enter the number of switches in the LAN(ex: 3): "))
        n_router = int(input("Enter the number of routers in the LAN(ex: 2): "))

        # Constructing DHCP configuration commands
        commands = f"""
            ip dhcp pool LAN{lan_id}
            network {network} {subnet_mask}
            default-router {ip}  # Assigning default gateway for the DHCP pool
            dns-server 8.8.8.8  # Configuring DNS server
            exit
            ip dhcp excluded-address {network_ip}.1 {network_ip}.{n_router + 1}  
            ip dhcp excluded-address {network_ip}.{255 - n_switch} {network_ip}.254
            """

        stdout, stderr = self.connection.exec(commands)
        if stderr:
            print(f"Error configuring DHCP: {stderr}")
        else:
            print("DHCP configuration successful")

        self.connection.close()
