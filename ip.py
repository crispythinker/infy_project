import socket

def get_local_ipv4():
    """Fetch and return the local IPv4 address of the machine."""
    try:
        # Create a socket and connect to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's DNS (used only to determine local IP)
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return "Could not retrieve local IPv4"

# Example usage
# local_ipv4 = get_local_ipv4()
# print(f"My local IPv4 address is: {local_ipv4}")
