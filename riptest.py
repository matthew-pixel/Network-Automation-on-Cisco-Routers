from netmiko import ConnectHandler
import time

# Router details (removed 'network' from the connection parameters)
routers = [
    {"device_type": "cisco_ios", "host": "192.168.32.129", "username": "admin", "password": "cisco", "secret": "cisco", "network": "192.168.32.128"},
    {"device_type": "cisco_ios", "host": "192.168.32.131", "username": "admin", "password": "cisco", "secret": "cisco", "network": "192.168.32.128"},
    {"device_type": "cisco_ios", "host": "192.168.32.145", "username": "admin", "password": "cisco", "secret": "cisco", "network": "192.168.32.144"}
]

# Function to configure RIP v2
def configure_rip(router):
    # Connect to the router
    print(f"Connecting to {router['host']}...")
    device = ConnectHandler(**{key: value for key, value in router.items() if key != 'network'})  # Remove 'network' key
    device.enable()

    # Configuration commands
    config_commands = [
        "router rip",
        "version 2",
        "no auto-summary",
        f"network {router['network']}",
    ]

    # Send configuration commands
    print(f"Configuring RIP on {router['host']}...")
    device.send_config_set(config_commands)
    device.save_config()

    # Disconnect
    device.disconnect()
    print(f"RIP configuration complete on {router['host']}.\n")

# Configure routers 1 and 2 via SSH
for router in routers[:2]:
    configure_rip(router)

# For router 3, SSH is not configured. You can manually configure this or set up SSH if needed.
print("Router 3 does not have SSH configured. Please manually configure it or set up SSH for automation.")
