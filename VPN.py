from netmiko import ConnectHandler

# Define Router 1 (HQ)
router1 = {
    'device_type': 'cisco_ios',
    'host': '192.168.32.129',
    'username': 'admin',
    'password': 'cisco',
    'secret': 'cisco'
}

# Define Router 2 (Branch)
router2 = {
    'device_type': 'cisco_ios',
    'host': '192.168.32.131',
    'username': 'admin',
    'password': 'cisco',
    'secret': 'cisco'
}

# VPN Configuration Parameters
peer_ip = "192.168.32.131"  # Remote peer (Branch)
local_ip = "192.168.32.129"  # Local router (HQ)
pre_shared_key = "MySecretKey123"
access_list = "100"
interface = "gigabitEthernet 0/0"

# VPN Configuration Commands for Router 1 (HQ)
vpn_config_1 = [
    "crypto isakmp policy 10",
    "encryption aes 256",
    "hash sha",
    "authentication pre-share",
    "group 2",
    "lifetime 86400",
    "exit",
    f"crypto isakmp key {pre_shared_key} address {peer_ip}",
    f"crypto ipsec transform-set MYSET esp-aes esp-sha-hmac",
    "mode tunnel",
    "exit",
    f"crypto map MYMAP 10 ipsec-isakmp",
    f"set peer {peer_ip}",
    "set transform-set MYSET",
    f"match address {access_list}",
    "exit",
    f"interface {interface}",
    "crypto map MYMAP",
    "exit",
    f"access-list {access_list} permit ip 10.1.1.0 0.0.0.255 10.2.2.0 0.0.0.255"
]

# VPN Configuration Commands for Router 2 (Branch)
vpn_config_2 = [
    "crypto isakmp policy 10",
    "encryption aes 256",
    "hash sha",
    "authentication pre-share",
    "group 2",
    "lifetime 86400",
    "exit",
    f"crypto isakmp key {pre_shared_key} address {local_ip}",
    f"crypto ipsec transform-set MYSET esp-aes esp-sha-hmac",
    "mode tunnel",
    "exit",
    f"crypto map MYMAP 10 ipsec-isakmp",
    f"set peer {local_ip}",
    "set transform-set MYSET",
    f"match address {access_list}",
    "exit",
    f"interface {interface}",
    "crypto map MYMAP",
    "exit",
    f"access-list {access_list} permit ip 10.2.2.0 0.0.0.255 10.1.1.0 0.0.0.255"
]

# Function to apply configuration
def configure_router(router, config_commands):
    try:
        print(f"Connecting to {router['host']}...")
        net_connect = ConnectHandler(**router)
        net_connect.enable()  # Enter enable mode
        net_connect.send_config_set(config_commands)
        print(f"VPN configured successfully on {router['host']}")
        net_connect.disconnect()
    except Exception as e:
        print(f"Failed to configure {router['host']}: {e}")

# Apply configuration to both routers
configure_router(router1, vpn_config_1)
configure_router(router2, vpn_config_2)
