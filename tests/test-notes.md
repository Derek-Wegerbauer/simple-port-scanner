# Test Notes

Manual testing was performed in a controlled lab environment using systems owned by the author or used with authorization.

The original local test script was named `simple_port_scanner.py`. In the GitHub repository, the main script is stored as `src/port_scanner.py`.

## Test Environment

- Scanner system: Main Windows laptop
- Remote Windows target: Secondary Windows laptop
- Linux target: Raspberry Pi Zero WH
- Language: Python 3.x
- Terminal: VS Code terminal / command line
- Network: Local private lab network

## Test Cases

| Test Case | Run On | Target | Test Area | Test Case Description | Command / Input | Expected Result | Observed Result | Status |
|---|---|---|---|---|---|---|---|---|
| TC-01 | Main Laptop | N/A | CLI | Help menu displays usage information | `python simple_port_scanner.py -h` | Usage text displays supported arguments and options | Help menu displayed correctly with usage syntax, target argument, and supported command-line options | Passed |
| TC-02 | Main Laptop | N/A | CLI | Missing required arguments are handled | `python simple_port_scanner.py` | argparse error and non-zero exit | Error displayed indicating that the required target argument was missing and usage information was shown | Passed |
| TC-03 | Main Laptop | localhost | CLI | Mutual exclusivity is enforced for scan options | `python simple_port_scanner.py localhost --common --ports 1-10` | Error indicating conflicting arguments | Error displayed stating that `--ports` is not allowed when `--common` is specified | Passed |
| TC-04 | Main Laptop | localhost | Validation | Invalid port range is rejected | `python simple_port_scanner.py localhost --ports 100-20` | Error message explaining that the start port must be less than or equal to the end port | Error displayed: `Port range start must be less than or equal to end.` | Passed |
| TC-05 | Main Laptop | localhost | Validation | Timeout value validation | `python simple_port_scanner.py localhost --common --timeout 0` | Error indicating timeout must be greater than 0 | Error displayed stating that `--timeout` must be a number greater than 0 and execution stopped | Passed |
| TC-06 | Main Laptop | localhost / 127.0.0.1 | Core Functionality | Baseline localhost scan using common ports | `python simple_port_scanner.py localhost --common` | Open and closed/filtered ports are reported correctly | Scan completed successfully and reported the status of common ports | Passed |
| TC-07 | Main Laptop | localhost / 127.0.0.1 | Output Filtering | Open-only output filtering | `python simple_port_scanner.py localhost --common --open-only` | Only open ports are displayed with a summary count | Output displayed only open ports, reported 2 open ports, and completed successfully | Passed |
| TC-08A | Secondary Windows Laptop | Local HTTP service | Remote Service Setup | Python HTTP server is started on port 8000 | `python -m http.server 8000 --bind 0.0.0.0` | HTTP server listens on port 8000 | HTTP server started successfully and listened on `0.0.0.0:8000` | Passed |
| TC-08B | Main Laptop | Secondary Windows laptop / 192.168.0.84 | Network | Remote HTTP service detection | `python simple_port_scanner.py 192.168.0.84 --ports 8000-8000` | Port 8000 is reported as open | Scanner successfully detected TCP port 8000 as open on the remote Windows laptop | Passed |
| TC-09A | Raspberry Pi Zero WH | Local SSH service | Remote Service Setup | SSH service is verified on Raspberry Pi | `sudo systemctl status ssh` | SSH service is active and running | SSH service showed `active (running)` | Passed |
| TC-09B | Main Laptop | Raspberry Pi Zero WH / 192.168.0.234 | Network | Raspberry Pi SSH detection | `python simple_port_scanner.py 192.168.0.234 --ports 22-22` | Port 22 is reported as open | Scanner successfully detected TCP port 22 as open on the Raspberry Pi running OpenSSH | Passed |
| TC-10 | Main Laptop | Raspberry Pi Zero WH | Network | Closed/filtered port detection | `python simple_port_scanner.py 192.168.0.234 --ports 9999-9999` | Port is reported as closed/filtered | Scanner reported the selected port as closed/filtered | Passed |

## Screenshot Evidence

Selected screenshots are available in the `screenshots/` folder.

Included screenshots:

- `TC-04_invalid-port-range.png`
- `TC-07_open-only_localhost.png`
- `TC-08A_http-server-running.jpg`
- `TC-08B_remote-port-8000-open.png`
- `TC-09A_raspberry-pi-ssh-running.png`
- `TC-09B_raspberry-pi-ssh-detected.png`

## Notes

Testing focused on correctness, input validation, error handling, output filtering, and safe use in an authorized lab environment.

The scanner is intentionally simple and does not include stealth, evasion, exploitation, credential attacks, service fingerprinting, or banner grabbing.

All testing was performed against localhost, lab systems, or systems owned by the author.
