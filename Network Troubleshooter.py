from netmiko import ConnectHandler
from datetime import datetime

# Define router details (Router 3 does not have SSH)
routers = [
    {"device_type": "cisco_ios", "host": "192.168.32.129", "username": "admin", "password": "cisco", "secret": "cisco"},
    {"device_type": "cisco_ios", "host": "192.168.32.131", "username": "admin", "password": "cisco", "secret": "cisco"},
    {"device_type": "cisco_ios", "host": "192.168.32.145", "username": "admin", "password": "cisco", "secret": "cisco"}
]

# Function to check router connectivity and troubleshoot
def troubleshoot_router(router):
    print(f"\n🔍 Connecting to {router['host']}...")
    
    try:
        # Connect via SSH
        device = ConnectHandler(**router)
        device.enable()

        # Run troubleshooting commands
        print(f"✅ Connected to {router['host']}")

        # Check RIP configuration
        print("\n🔹 Checking RIP configuration...")
        output = device.send_command("show ip protocols")
        print(output if output else "❌ RIP not configured")

        # Check RIP learned routes
        print("\n🔹 Checking RIP routes...")
        output = device.send_command("show ip route rip")
        print(output if output else "❌ No RIP routes found")

        # Check RIP neighbors
        print("\n🔹 Checking RIP neighbors...")
        output = device.send_command("show ip rip neighbors")
        print(output if output else "❌ No RIP neighbors detected")

        # Ping test to other routers
        for target in routers:
            if target["host"] != router["host"]:  # Don't ping itself
                print(f"\n🔹 Pinging {target['host']} from {router['host']}...")
                ping_result = device.send_command(f"ping {target['host']}")
                print(ping_result)

        # Disconnect
        device.disconnect()
        print(f"\n✅ Troubleshooting complete for {router['host']}\n")

    except Exception as e:
        print(f"❌ Unable to connect to {router['host']}. Error: {str(e)}")

# Run troubleshooting for routers with SSH
for router in routers[:2]:  # Router 3 does not have SSH
    troubleshoot_router(router)

print("⚠️ Router 3 (192.168.32.145) does not have SSH. Manual troubleshooting required.")
