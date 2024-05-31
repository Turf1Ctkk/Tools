import subprocess

def ping_ip(ip):
    try:
        # Ping the IP address with a timeout of 1 second
        output = subprocess.check_output(['ping', '-c', '1', '-W', '1', ip], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    base_ip = "192.168.1."
    successful_ips = []

    for i in range(1, 255):
        ip = f"{base_ip}{i}"
        print(f"Pinging {ip}...")
        if ping_ip(ip):
            print(f"IP {ip} is reachable.")
            successful_ips.append(ip)
        else:
            print(f"IP {ip} is not reachable.")
    
    print("\nSuccessfully pinged IPs:")
    for ip in successful_ips:
        print(ip)

if __name__ == "__main__":
    main()
