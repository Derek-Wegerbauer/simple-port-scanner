"""
Simple Port Scanner (TCP connect scan)

Educational and authorized testing only.

Scans a single target (IP address or hostname) across either:
- A built-in list of common ports, or
- A user-specified port range

Author: Derek Wegerbauer
"""

import argparse
import socket
import sys
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional

COMMON_PORTS: List[int] = [
    20, 21, 22, 23, 25, 53, 67, 68, 69,
    80, 110, 111, 123, 135, 137, 138, 139,
    143, 161, 389, 443, 445, 465, 587, 636,
    993, 995, 1433, 1521, 2049, 3306, 3389,
    5432, 5900, 6379, 8080, 8443, 9200,
]

@dataclass
class ScanResult:
    port: int
    status: str # "Open" or "Closed/Filtered"

def parse_port_range(port_range: str) -> Tuple[int, int]:
    """
    Parse a port range like "1-1024" into (start, end).
    """
    try:
        parts = port_range.split("-")
        
        if len(parts) != 2:
            raise ValueError
                
        start = int(parts[0].strip())
        end = int(parts[1].strip())
    
    except Exception as exc:
        raise ValueError(
            f"Invalid port range '{port_range}'. Use start-end, example: 1-1024"
        ) from exc

    if start < 1 or end < 1 or start > 65535 or end > 65535:
        raise ValueError("Ports must be between 1 and 65535.")
    
    if start > end:
        raise ValueError(
            "Port range start must be less than or equal to end."
        )
    
    return start, end


def resolve_target(target: str) -> str:
    """
    Resolve a hostname or IP to a single IPv4 address string.
    If the hostname has multiple A records, the resolver chooses one. 
    """
    try:
        return socket.gethostbyname(target)
    except socket.gaierror as exc:
        raise ValueError(
            f"Could not resolve target '{target}'."
        ) from exc
    

def check_tcp_port(ip: str, port: int, timeout: float) -> ScanResult:
    """
    Attempt a TCP connection. 
    
    If connect succeeds:
      Open
    
    Otherwise: 
      Closed/Filtered
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            return ScanResult(port=port, status="Open")
        
        return ScanResult(port=port, status="Closed/Filtered")
    
    except (socket.timeout, OSError):
        return ScanResult(port=port, status="Closed/Filtered")
    
    finally:
        sock.close()


def build_port_list(
    use_common: bool, 
    port_range: Optional[str]
) -> List[int]:
    
    if use_common:
        return sorted(set(COMMON_PORTS))
    
    if not port_range:
        raise ValueError(
            "You must specify either --common or --ports START-END."
        )

    start, end = parse_port_range(port_range)
    
    return list(range(start, end + 1))


def format_result_line(res: ScanResult) -> str:
    return f"Port {res.port}: {res.status}"


def main() -> int:
    
    parser = argparse.ArgumentParser(
        description="Simple TCP port scanner (authorized use only)"
    )
    
    parser.add_argument(
        "target",
        help="Target hostname or IPv4 address (example: 192.168.1.10 or example.com)"
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument(
        "--common",
        action="store_true",
        help="Scan a built-in list of common ports"
    )
    
    group.add_argument(
        "--ports",
        metavar="START-END",
        help="Scan a port range (example: 1-1024)"
    )
    
    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="Socket timeout in seconds (default: 0.5)"
    )
    
    parser.add_argument(
        "--open-only",
        action="store_true",
        help="Display only open ports in output"
    )

    args = parser.parse_args()

    # Timeout validation
    if args.timeout <= 0:
        print(
            "Error: --timeout must be a number greater than 0.", 
            file=sys.stderr
        )
        return 2

    try:
        ip = resolve_target(args.target)
        ports = build_port_list(args.common, args.ports)
    
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    
    print(f"Scan Target: {args.target} ({ip})")
    
    if args.common:
        print("Ports: common list")
    else:
        print(f"Ports: {ports[0]}-{ports[-1]}")
    
    print(f"Timeout: {args.timeout} seconds")

    if args.open_only:
        print("Display mode: open ports only")
    else:
        print("Display mode: all ports")

    print("Notice: Only scan systems you own or have permission to test.")

    start_time = time.time()

    open_count = 0
    
    for port in ports:
        
        result = check_tcp_port(
            ip, 
            port, 
            args.timeout
        )
        
        if result.status == "Open":
            open_count += 1

        if (not args.open_only) or (result.status == "Open"):
            print(format_result_line(result))

    elapsed = time.time() - start_time

    if args.open_only:
        print(f"Open ports found: {open_count}")

    print(f"Scan completed in {elapsed:.2f} seconds")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
