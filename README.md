# AutoRecon

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Kali%20%7C%20Ubuntu%20%7C%20Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Learning%20Project-orange)

A small Python tool that scans a handful of common TCP ports, checks HTTP security headers on a local test site, and saves what it finds in a JSON report.

**This is my first cybersecurity project.** I built it to understand how recon works under the hood instead of just running tools I don't understand. It's a starter version, not a full vulnerability scanner, and I'm improving it one feature at a time.

---

## Please read this first

Only scan systems you own or have clear permission to test. Scanning other people's machines can be illegal, even if you mean no harm.

Safe things to practice on:

- Your own computer (`127.0.0.1` or `localhost`)
- Your own lab, such as DVWA or Metasploitable running on your network
- `scanme.nmap.org`, which the Nmap project provides for people to practice on (go easy on it, no repeated or aggressive scans)

I'm not responsible for how anyone uses this code. It's meant for learning and authorized testing.

---

## What it does

- Resolves a hostname to an IP address
- Checks 9 common TCP ports using Python sockets
- Looks for missing security headers on a local test website
- Saves the results (target, IP, timestamp, open ports, HTTP findings) to `autorecon_report.json`
- Handles bad hostnames, DNS failures and connection errors without crashing

For the HTTP check, I limited it to `localhost` and `127.0.0.1` on purpose. I didn't want a beginner project that could be pointed at random websites by accident.

---

## Screenshots

Running the scanner against `scanme.nmap.org` on Kali Linux:

![AutoRecon running in the terminal](https://github.com/vimal-proworkspace/Auto-recon-/raw/refs/heads/main/images/AutoRecon_running_in_the_terminal)

The report it generated:

![AutoRecon JSON report](https://github.com/vimal-proworkspace/Auto-recon-/raw/refs/heads/main/images/AutoRecon_JSON_report)

It found ports 22 (SSH) and 80 (HTTP) open, which is what I expected for that host.

---

## Getting started

You'll need Python 3.8+ and pip.

**1. Clone the repo**

```bash
git clone https://github.com/<your-username>/autorecon.git
cd autorecon
```

**2. Create and activate a virtual environment**

Kali / Ubuntu / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

You'll know it worked when `(venv)` shows up at the start of your prompt:

```
(venv) ┌──(kali㉿kali)-[~/autorecon]
```

**3. Install the dependency**

```bash
pip install requests
```

---

## Running it

```bash
python3 autorecon.py
```

For your very first test, type `127.0.0.1` when it asks for a target. That scans your own machine, so there's no risk.

Here's what a run looks like:

```
=== AutoRecon Security Scanner ===
Enter your authorized target IP or hostname: scanme.nmap.org

Scanning 45.33.32.156...
[+] Port 22: OPEN
[+] Port 80: OPEN
Check HTTP headers on a local test website? (y/n): y
Enter the URL of your local test website:
For this beginner version, use a local test website only.

Scan complete. Report saved to autorecon_report.json
```

### Trying the header check

Start a simple local web server in another terminal:

```bash
python3 -m http.server 8000
```

Run AutoRecon again, answer `y`, and enter `http://127.0.0.1:8000`. It will tell you which of these headers are missing:

- `Content-Security-Policy`
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Strict-Transport-Security`

---

## Sample report

```json
{
    "target": "scanme.nmap.org",
    "resolved_ip": "45.33.32.156",
    "scan_time": "2026-10-20T10:52:06.802565-04:00",
    "open_ports": [
        { "port": 22, "status": "Open" },
        { "port": 80, "status": "Open" }
    ],
    "http_check": null
}
```

`http_check` is `null` when I skipped the header check or gave a non-local URL.

An open port just means a service is accepting connections. It doesn't mean there's a vulnerability.

---

## Ports it checks

| Port | Service |
|------|---------|
| 21 | FTP |
| 22 | SSH |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 445 | SMB |
| 3306 | MySQL |
| 8080 | HTTP (alternate) |

---

## How it works

1. `main()` asks for a target and resolves it with `socket.gethostbyname()`.
2. `scan_ports()` tries a TCP connection to each port using `connect_ex()` with a 0.5 second timeout. A result of `0` means the port is open.
3. If I ask for it, `check_http_headers()` sends a GET request with `requests` and lists any missing security headers.
4. Everything gets written to a JSON file with `json.dump()`.

---

## What I learned

- How TCP connections work, and how a script can tell if a port is open or closed
- Why security headers matter and how to spot when they're missing
- How to structure scan results as JSON so they're easy to use later
- Handling errors properly, like DNS failures, timeouts and bad input
- Why scope and authorization come before everything else in security testing

---

## What it can't do (yet)

I want to be upfront about the limits so nobody mistakes this for a real scanner:

- It doesn't identify services or versions
- It doesn't find vulnerabilities, only open ports and missing headers
- The port list is fixed, with no custom ranges yet
- TCP only, no UDP
- Scanning is sequential, so it would be slow with a big port list
- HTTP checks only work on localhost
- It makes no attempt to be stealthy

For real assessments, use a mature tool like [Nmap](https://nmap.org/).

---

## What I want to build next

- [ ] Command-line options for target and port range (`argparse`)
- [ ] Service identification for open ports
- [ ] Faster scanning with threads
- [ ] A formatted HTML report
- [ ] Risk explanations and fix recommendations
- [ ] Testing against my own vulnerable lab
- [ ] Unit tests
- [ ] Documenting real test results in this repo

---

## Project structure

```
autorecon/
├── autorecon.py
├── autorecon_report.json
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## About me

I'm **Your Name**, learning cybersecurity and building projects to understand how things really work.

- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [your-profile](https://linkedin.com/in/your-profile)

Since this is my first project, I'd really appreciate feedback, ideas or corrections. If it helped you, a star on the repo means a lot.

---

## License

MIT License. See the `LICENSE` file for details.

## Thanks to

- The [Nmap project](https://nmap.org/) for `scanme.nmap.org` and the inspiration
- [Kali Linux](https://www.kali.org/) for the testing environment
- The [Requests](https://requests.readthedocs.io/) library
