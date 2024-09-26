from Switch import Switch
from Router import Router
from GetDetails import Config_Manager


def main():
    # Initialize the configuration manager and load device configurations
    device_loader = Config_Manager()
    devices = device_loader.load('NetworkDetails.json')

    print("""
    Welcome to Tavi's Main Menu:

    Available options:
    1. Configure a device.
    2. Exit the application.
    """)

    choice = input("Enter your choice: ")
    if choice == '1':
        # Prompt for the device IP to configure
        target_device = input("Enter the IP of the device you want to configure: ")
        device_not_found = True

        for device in devices:
            if device_not_found:
                try:
                    # Check if the IP matches and call the appropriate configuration function
                    if device['ip'] == target_device:
                        device_not_found = False
                        if "router" in device['type'].lower():
                            configRouter(device)
                        elif "sw" in device['type'].lower():
                            configSwitch(device)
                except TimeoutError or ConnectionError:
                    print("Connection failed: Could not reach the target or network.")

        if device_not_found:
            raise ValueError(
                f"No device with the IP {target_device} was found. Check the IP or add the device to the file")

    elif choice == '2':
        # Exit the application
        print("Closing the application... Goodbye")
        exit()

    else:
        raise ValueError("Wrong Option. Please try 1 or 2")


def configRouter(device):
    # Configure Router
    router = Router(device['name'], device['ip'], device['username'], device['password'], device['privileged_password'])

    while True:
        print("""
        Router Configuration Options:
        1. Configure RIPv2.
        2. Configure DHCP.
        3. Configure HSRP.
        4. Ping to ...
        5. Back to Tavi's Main Menu.
        """)

        config_choice = input("Enter your choice: ")
        if config_choice == '1':
            router.rip()
        elif config_choice == '2':
            router.dhcp(device['ip'])
        elif config_choice == '3':
            router.hsrp()
        elif config_choice == '4':
            router.ping_Device()
        elif config_choice == '5':
            main()
            # Return to main menu
            return
        else:
            print("Please enter a valid option.")


def configSwitch(device):
    # Configure Switch
    switch = Switch(device['name'], device['ip'], device['username'], device['password'], device['privileged_password'])

    while True:
        print("""
        Switch Configuration Options:
        1. Set up a VLAN.
        2. Configure STP.
        3. Configure security.
        4. Configure HSRP (only for multilayer switches).
        5. Ping to ...
        6. Back to Tavi's Main Menu.
        """)

        config_choice = input("Enter your choice: ")
        if config_choice == '1':
            switch.vlan()
        elif config_choice == '2':
            switch.stp()
        elif config_choice == '3':
            switch.security()
        elif config_choice == '4':
            if "multilayer" not in device['name'].lower():
                print("This is not a multilayer switch, so it cannot act as a router.")
            else:
                switch.hsrp()
        elif config_choice == '5':
            switch.ping_Device()
        elif config_choice == '6':
            main()
            # Return to main menu
            return
        else:
            # Handle invalid options
            print("Please enter a valid choice.")
