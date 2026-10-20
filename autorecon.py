
import socket
import requests
import json
from datetime import datetime

def scan_ports(target, ports):
    results = []

    print(f"\nScanning {target}...")

    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                status = s.connect_ex((target, port))

                if status == 0:
                    result = {
                        "port": port,
                        "status": "Open"
                    }
                    results.append(result)
                    print(f"[+] Port {port}: OPEN")

        except (socket.gaierror, OSError) as error:
            print(f"Error scanning port {port}: {error}")

    return results


def check_http_headers(url):
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        security_headers = [
            "Content-Security-Policy",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "Strict-Transport-Security"
        ]

        findings = []

        for header in security_headers:
            if header not in headers:
                findings.append({
                    "header": header,
                    "status": "Missing"
                })
                print(f"[-] Missing header: {header}")
            else:
                print(f"[+] Present header: {header}")

        return {
            "url": url,
            "http_status": response.status_code,
            "missing_headers": findings
        }

    except requests.RequestException as error:
        print(f"HTTP check failed: {error}")
        return {"url": url, "error": str(error)}


def main():
    print("=== AutoRecon Security Scanner ===")

    target = input("Enter your authorized target IP or hostname: ").strip()

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Invalid hostname or DNS resolution failed.")
        return

    # Scan only the target you own or are authorized to test.
    ports = [21, 22, 25, 53, 80, 443, 445, 3306, 8080]

    open_ports = scan_ports(ip, ports)

    http_result = None

    # HTTP checks are performed only when explicitly requested.
    choice = input("Check HTTP headers on a local test website? (y/n): ")
    if choice.lower() == "y":
        url = input("Enter the URL of your local test website: ").strip()

        if url.startswith(("http://127.0.0.1", "http://localhost",
                           "https://127.0.0.1", "https://localhost")):
            http_result = check_http_headers(url)
        else:
            print("For this beginner version, use a local test website only.")

    report = {
        "target": target,
        "resolved_ip": ip,
        "scan_time": datetime.now().astimezone().isoformat(),
        "open_ports": open_ports,
        "http_check": http_result
    }

    filename = "autorecon_report.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"\nScan complete. Report saved to {filename}")


if __name__ == "__main__":
    main()
