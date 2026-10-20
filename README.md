# AutoRecon

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tested on](https://img.shields.io/badge/Tested%20on-Kali%20Linux-557C94?logo=kalilinux&logoColor=white)
![Status](https://img.shields.io/badge/Status-Beginner%20Project%20%7C%20Actively%20Maintained-orange)

A small Python tool that scans a handful of common TCP ports, checks HTTP security headers on a local test site, and saves what it finds in a JSON report.

**This is my first cybersecurity project, and I'm actively improving it.** I built it to understand how recon works under the hood instead of just running tools I don't understand. It's a beginner learning project and a starter version, not a full vulnerability scanner. I keep it maintained and add features one at a time.

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
- Checks a local test website for four common security headers and reports which are present or missing
- Saves the results (target, IP, timestamp, open ports, HTTP findings) to `autorecon_report.json`
- Handles bad hostnames, DNS failures and connection errors without crashing

For the HTTP check, I limited it to `localhost` and `127.0.0.1` on purpose. I didn't want a beginner project that could be pointed at random websites by accident.

---

## Project status

AutoRecon is both a **beginner learning project** and an **actively maintained project**. It is small and limited by design, and I'm improving it step by step (see the roadmap below).

---

## Testing

I have manually tested the following on **Kali Linux**:

- The nine-port TCP scan (against `scanme.nmap.org` and my own machine)
- The HTTP security header check (against a local test server)
- JSON report generation
- Error handling for invalid hostnames, DNS failures, connection errors and non-local URLs

I have **not** tested AutoRecon on Windows, Ubuntu or macOS, so I can't promise it works there. There are no automated tests yet (they're on the roadmap).

---

## Screenshots

Running the scanner against `scanme.nmap.org` on Kali Linux:

![AutoRecon running in the terminal](https://github.com/vimal-proworkspace/Auto-recon-/raw/refs/heads/main/images/AutoRecon_running_in_the_terminal)

The report it generated:

![AutoRecon JSON report](https://github.com/vimal-proworkspace/Auto-recon-/raw/refs/heads/main/images/AutoRecon_JSON_report)

It found ports 22 (SSH) and 80 (HTTP) open, which is what I expected for that host.

---

## Getting started

You'll need Python 3.8+ and pip. I developed and tested it on Kali Linux. I haven't tested other Python versions, so 3.8 is the minimum I'm documenting for now.

**1. Clone the repo**

```bash
git clone https://github.com/vimal-proworkspace/Auto-recon-.git
cd Auto-recon-
```

**2. Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

You'll know it worked when `(venv)` shows up at the start of your prompt.

**3. Install the dependency**

```bash
pip install requests
```

`requests` is the only external dependency. Everything else (`socket`, `json`, `datetime`) comes with Python.

---

## Running it

```bash
python3 autorecon.py
```

For your very first test, type `127.0.0.1` when it asks for a target. That scans your own machine, so there's no risk.

### Example terminal output

This is an example run, and your output will differ depending on the target and which ports are open:

```
=== AutoRecon Security Scanner ===
Enter your authorized target IP or hostname: scanme.nmap.org

Scanning 45.33.32.156...
[+] Port 22: OPEN
[+] Port 80: OPEN
Check HTTP headers on a local test website? (y/n): n

Scan complete. Report saved to autorecon_report.json
```

### Trying the header check

Start a simple local web server in another terminal:

```bash
python3 -m http.server 8000
```

Run AutoRecon again, answer `y`, and enter `http://127.0.0.1:8000`. It checks for these headers and reports each one as present or missing:

- `Content-Security-Policy`
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Strict-Transport-Security`

Example output (Python's simple server doesn't send any of these headers, so all four are reported missing):

```
[-] Missing header: Content-Security-Policy
[-] Missing header: X-Content-Type-Options
[-] Missing header: X-Frame-Options
[-] Missing header: Strict-Transport-Security
```

---

## Example report

This is an example of the generated `autorecon_report.json`. Your values will differ:

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

`http_check` is `null` when I skipped the header check or gave a non-local URL. When the header check runs, it contains the URL, the HTTP status code and a list of any missing headers.

**An open port does not necessarily mean there is a vulnerability.** It only means a service is accepting connections. Many open ports (like 80 or 443 on a web server) are completely normal. Whether a service is actually a problem depends on its version, configuration and purpose, and AutoRecon doesn't assess that.

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
3. If I ask for it, `check_http_headers()` sends a GET request with `requests` and reports which security headers are present or missing.
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
- It has only been tested on Kali Linux

For real assessments, use a mature tool like [Nmap](https://nmap.org/).

---

## Roadmap

Planned features. Nothing below is implemented yet, so nothing is checked off:

- [ ] Command-line options for target and port range (`argparse`)
- [ ] Service identification for open ports
- [ ] Faster scanning with threads (multithreading)
- [ ] A formatted HTML report
- [ ] Risk explanations and fix recommendations
- [ ] Testing against my own vulnerable lab
- [ ] Unit tests
- [ ] Documenting real test results in this repo
- [ ] Add a `requirements.txt`
- [ ] Add a `LICENSE` file

---

## Project structure

```
Auto-recon-/
├── images/
│   └── (screenshots used in this README)
├── autorecon.py
└── README.md
```

`autorecon_report.json` is created in the folder where you run the script.

---

## About me

I'm **Vimal**, learning cybersecurity and building projects to understand how things really work.

- GitHub: [@vimal-proworkspace](https://github.com/vimal-proworkspace)
- LinkedIn: [vimal-annadurai](https://www.linkedin.com/in/vimal-annadurai/)

Since this is my first project, I'd really appreciate feedback, ideas or corrections. If it helped you, a star on the repo means a lot.

---

## License

This repository does not include a license file yet. I plan to add the MIT License, and I'll update this section once the `LICENSE` file is in the repo. Until then, default copyright applies.

## Thanks to

- The [Nmap project](https://nmap.org/) for `scanme.nmap.org` and the inspiration
- [Kali Linux](https://www.kali.org/) for the testing environment
- The [Requests](https://requests.readthedocs.io/) library
