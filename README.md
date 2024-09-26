Here is a suggested `README.md` for your GitHub repository that explains how to use the Python-based network management project:

---

# Network Management Automation

This project provides a Python-based automation tool for managing network devices such as switches and routers using SSH. It allows you to automate common network configuration tasks like configuring HSRP, DHCP, VLANs, RIP, and STP, as well as basic device security and connectivity testing.

## Features

- **HSRP Configuration** on routers
- **VLAN and STP Setup** on switches
- **DHCP Pool Configuration** on routers
- **RIP Routing Protocol** setup
- **Port Security** configuration on switches
- **Ping Connectivity Testing** to verify network reachability
- **Singleton-based configuration management** to ensure a consistent configuration load from `NetworkDetails.json`

## File Structure

- **`NetworkDetails.json`**: This file contains a list of network devices (routers, switches) and their respective login credentials and IP addresses.
- **`GetDetails.py`**: Provides the `Config_Manager` class for loading network device details from `NetworkDetails.json`.
- **`Connection.py`**: Contains the `NetworkSession` class to manage SSH connections to network devices.
- **`Device.py`**: Provides the `Device` class for abstracting common device operations such as HSRP and connectivity testing.
- **`Router.py`**: Extends `Device` class to support router-specific operations like DHCP and RIP configuration.
- **`Switch.py`**: Extends `Device` class to support switch-specific operations like VLAN, STP, and port security configuration.
- **`Main.py`**: Entry point to run the network management tool.
- **`Menu.py`**: Contains the menu-driven interface for interacting with the tool.

## Setup

### Prerequisites

1. Install Python 3.x
2. Install the required Python libraries:
   ```bash
   pip install paramiko
   ```

3. Make sure you have access to the devices you want to configure via SSH.

### NetworkDetails.json

This file contains the details of network devices including switches and routers. Here is an example of how it's structured:

```json
[
  {
    "type": "router",
    "name": "R1",
    "ip": "192.168.1.1",
    "username": "admin",
    "password": "cisco",
    "privileged_password": "class"
  },
  {
    "type": "normal_sw",
    "name": "Switch1",
    "ip": "192.168.1.251",
    "username": "admin",
    "password": "cisco",
    "privileged_password": "class"
  }
]
```

Each device entry includes:
- `type`: Indicates whether the device is a `router`, `normal_sw` (normal switch), or `multilayer_sw`.
- `name`: The name identifier of the device.
- `ip`: The IP address of the device.
- `username`: The login username for SSH access.
- `password`: The login password for SSH access.
- `privileged_password`: The password to enter privileged (enable) mode.

### Running the Application

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/network-management-tool.git
   ```
   
2. Modify the `NetworkDetails.json` file with your actual network device details.

3. Run the main script:
   ```bash
   python Main.py
   ```

This will launch a menu-driven interface to interact with network devices.

## Usage

### HSRP Configuration

To configure HSRP on a router:
1. Select the router from the menu.
2. Provide the necessary interface, standby ID, virtual router IP, and priority.
3. HSRP will be configured with the provided values.

### VLAN Configuration

To configure VLAN on a switch:
1. Select the switch from the menu.
2. Provide the VLAN ID and name.
3. VLAN will be created with the specified details.

### DHCP Configuration

To configure a DHCP pool on a router:
1. Select the router from the menu.
2. Provide the LAN ID, network, and subnet mask.
3. DHCP will be configured and specific IP ranges will be excluded.

### RIP Configuration

To configure RIP on a router:
1. Select the router from the menu.
2. Enter multiple networks to add to RIP.
3. Optionally enable static route redistribution.

### Ping Connectivity

To test network connectivity:
1. Select a device and provide the IP to ping.
2. The script will attempt to ping the target IP and provide results.

### Adding New Devices

To add new devices to the tool, simply update the `NetworkDetails.json` file with the new device's information.
