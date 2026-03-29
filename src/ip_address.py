import socket
import urllib.request
import re
import ssl


def get_local_ip():
    """Retrieves the local IP address (LAN) of the machine."""
    try:
        # Create a dummy socket to find the active network interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_public_ip_robust():
    """Retrieves the Public IP using text-based services to avoid JSON errors."""
    # Bypasses SSL certificate verification issues common on Windows
    ctx = ssl._create_unverified_context()

    # List of reliable plain-text IP services
    urls = [
        'https://api.ipify.org',
        'https://ifconfig.me',
        'https://icanhazip.com'
    ]

    for url in urls:
        try:
            # Added a browser-like User-Agent to prevent bot-blocking
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
                # Read response and strip whitespace/newlines
                ip = response.read().decode('utf-8').strip()

                # Use Regex to confirm the result is a valid IPv4 address
                if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', ip):
                    return ip
        except Exception:
            continue
    return None


if __name__ == "__main__":
    print("Checking network status...")
    local_ip = get_local_ip()
    public_ip = get_public_ip_robust()

    print("-" * 40)
    print(f"LOCAL IP (LAN):  {local_ip}")

    if public_ip:
        print(f"PUBLIC IP (WAN): {public_ip}")
        print("STATUS:          Internet Connected")
    else:
        print("PUBLIC IP:       Detection Failed (Format/Network Error)")
    print("-" * 40)
