# Simple Port Scanner

A Python TCP connect scanner for educational and authorized network testing.

## Overview

This project is a command-line TCP port scanner written in Python. It scans a single target, such as an IPv4 address or hostname, and checks whether selected TCP ports are open or closed/filtered.

The scanner was created as a learning project to practice Python scripting, networking fundamentals, command-line tool development, and ethical security testing.

A full project write-up with testing notes, design decisions, screenshots, and future improvements is available in the `docs/` folder.

## Features

- Scan a target hostname or IPv4 address
- Scan a built-in list of common ports
- Scan a user-specified port range
- Configure socket timeout values
- Display all results or only open ports
- Basic input validation and error handling
- Clear command-line output

## Skills Demonstrated

- Python scripting
- Socket programming
- Command-line argument parsing with `argparse`
- TCP networking fundamentals
- Error handling and validation
- Ethical testing boundaries
- Project documentation

## Usage

Run the scanner from the project root directory:

```bash
python src/port_scanner.py TARGET --common
```

Example using the common port list:

```bash
python src/port_scanner.py 127.0.0.1 --common
```

Example using a port range:

```bash
python src/port_scanner.py 127.0.0.1 --ports 20-100
```

Example showing only open ports:

```bash
python src/port_scanner.py 127.0.0.1 --common --open-only
```

Example with a custom timeout:

```bash
python src/port_scanner.py 127.0.0.1 --ports 1-1024 --timeout 1
```

## Example Output

```text
Scan Target: 127.0.0.1 (127.0.0.1)
Ports: common list
Timeout: 0.5 seconds
Display mode: all ports
Notice: Only scan systems you own or have permission to test.
Port 20: Closed/Filtered
Port 21: Closed/Filtered
Port 22: Open
Port 23: Closed/Filtered
Scan completed in 0.12 seconds
```

## Screenshots

Selected screenshots from controlled lab testing are available in the `screenshots/` folder.

Examples include:

- Localhost open-only scan
- Invalid port range validation
- Remote Windows HTTP service detection
- Raspberry Pi SSH detection

## Project Structure

```text
simple-port-scanner/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   └── port_scanner.py
├── docs/
│   └── project-writeup.md
└── screenshots/
```

## Requirements

This project uses only the Python standard library.

No external Python packages are required.

## Ethical Notice

This tool is for educational use and authorized testing only. Only scan systems that you own or have explicit permission to test.

## Limitations

- IPv4 only
- TCP connect scan only
- Does not perform service detection
- Does not perform banner grabbing
- Does not identify firewall rules directly
- Results may show `Closed/Filtered` when a port is blocked, filtered, timed out, or closed

## Future Improvements

- Add IPv6 support
- Add banner grabbing
- Add CSV or JSON output
- Add logging to a file
- Add unit tests
- Add multithreading for faster scans
- Add more detailed documentation and screenshots

## Author

Derek Wegerbauer
