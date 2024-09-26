from Device import Device

class Switch(Device):  # Inheriting from 'Device'

    def vlan(self):
        # Configure VLAN
        self.connection.connect(self.enable_pass)

        vlan_id = input("Enter the ID of the VLAN you want to be created(ex: 10): ")
        vlan_name = input("Enter the name of the VLAN you want to create(ex: HR): ")

        vlan_commands = f"""
        vlan {vlan_id}
        name {vlan_name}
        """

        stdout, stderr = self.connection.exec(vlan_commands)

        if stderr:
            print(f"Error configuring VLAN: {stderr}")
        else:
            print("VLAN configuration successful")

        self.connection.close()

    def stp(self):
        # Configure STP
        self.connection.connect(self.enable_pass)

        primary_vlan = input("Enter the VLAN ID to set as primary(ex: 10) or press Enter to skip: ")
        secondary_vlan = input("Enter the VLAN ID to set as secondary(ex: 20) or press Enter to skip: ")

        stp_command = "spanning-tree mode rapid-pvst"

        if primary_vlan:
            stp_command += f"\nspanning-tree vlan {primary_vlan} root primary"
        if secondary_vlan:
            stp_command += f"\nspanning-tree vlan {secondary_vlan} root secondary"

        if stp_command != "spanning-tree mode rapid-pvst":
            stdout, stderr = self.connection.exec(stp_command)

            if stderr:
                print(f"Error configuring STP: {stderr}")
            else:
                print("STP configuration applied successfully.")
        else:
            print("No VLAN configuration entered. No changes were made.")

        self.connection.close()

    def security(self):
        # Configure Security
        self.connection.connect(self.enable_pass)  # Connect to the switch using privileged mode

        interface = input("Enter the name of the interface you want to apply security to(ex: Gi0/1): ")
        vlan = input("Please enter the name of the VLAN you want to be allowed to pass(ex: 10): ")

        security_commands = f"""
            int {interface}
            switchport mode access  # Set the interface as an access port
            switchport access vlan {vlan}  # Assign the VLAN to the interface
            switchport port-security  # Enable port security
            spanning-tree portfast edge default  # Enable PortFast for faster convergence
            spanning-tree portfast edge bpduguard default  # Enable BPDU Guard to protect against loops
            spanning-tree portfast edge default  # Reapply PortFast (redundant command)
        """

        stdout, stderr = self.connection.exec(security_commands)

        if stderr:
            print(f"Error configuring security: {stderr}")
        else:
            print("Security configuration successful")

        self.connection.close()
