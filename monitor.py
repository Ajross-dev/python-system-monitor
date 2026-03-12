#Simple System Monitor using psutil.

#Run:
# python monitor.py

#This prints a live updated snapshot of CPU, memory, disk, and network usage.


import argparse
import platform
import subprocess
import sys
import time

import psutil


def clear_screen() -> None:
    #Clear the terminal screen (cross-platform).
    cmd = "cls" if platform.system() == "Windows" else "clear"
    subprocess.run([cmd], shell=True)

def format_bytes(size: float, suffix: str = "B") -> str:
    #Convert bytes to a human-readable string.
    for unit in ["", "K", "M", "G", "T", "P"]: 
        if abs(size) < 1024.0: 
            return f"{size:3.1f}{unit}{suffix}" 
        size /= 1024.0 
    return f"{size:.1f}P{suffix}" 


def get_cpu_info(interval: float) -> str:
    #Return CPU usage and frequency info.
    cpu_percent = psutil.cpu_percent(interval=interval, percpu=False)
    cpu_freq = psutil.cpu_freq()
    freq_str = "n/a" 
    if cpu_freq:
        freq_str = f"{cpu_freq.current:.0f} MHz" 

    #Get per-core usage percentages.
    per_cpu = psutil.cpu_percent(interval=None, percpu=True)
    per_cpu_str = ", ".join(f"{p:.0f}%" for p in per_cpu)

    return (
        f"CPU Total: {cpu_percent:.0f}%   "
        f"Freq: {freq_str}\n"
        f"Per-core: {per_cpu_str}"
    )


def get_memory_info() -> str:
    #Return memory usage info.
    vm = psutil.virtual_memory()
    stm = psutil.swap_memory()

    return (
        f"Memory: {format_bytes(vm.used)}/{format_bytes(vm.total)} "
        f"({vm.percent:.0f}%)\n"
        f"Swap:   {format_bytes(stm.used)}/{format_bytes(stm.total)} "
        f"({stm.percent:.0f}%)"
    )


def get_disk_info() -> str:
    #Return disk usage info for each mounted partition.
    parts = psutil.disk_partitions(all=False)
    lines = []
    for p in parts:
        try:
            usage = psutil.disk_usage(p.mountpoint)
        except PermissionError:
            continue
        lines.append(
            f"{p.device} ({p.mountpoint}) {usage.percent:.0f}% "
            f"{format_bytes(usage.used)}/{format_bytes(usage.total)}"
        )
    return "\n".join(lines) if lines else "No disk partitions found."


def get_network_info(previous: psutil._common.snetio | None) -> tuple[str, psutil._common.snetio | None]:
    #Return network I/O delta since previous snapshot.
    current = psutil.net_io_counters(pernic=False)
    if previous is None:
        return "Network: (initializing stats)\n", current

    sent = current.bytes_sent - previous.bytes_sent
    recv = current.bytes_recv - previous.bytes_recv
    return (
        f"Network: ↑ {format_bytes(sent)}/s  ↓ {format_bytes(recv)}/s\n"
        f"Total: ↑ {format_bytes(current.bytes_sent)}  ↓ {format_bytes(current.bytes_recv)}",
        current,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple terminal-based system monitor using psutil.")
    parser.add_argument("--interval", "-i", type=float, default=1.0, help="Refresh interval in seconds")
    parser.add_argument("--once", action="store_true", help="Print one snapshot and exit")
    args = parser.parse_args()

    net_prev = None
    try:
        while True:
            clear_screen()
            print("=== System Monitor (press Ctrl+C to quit) ===\n")
            print(get_cpu_info(interval=args.interval))
            print()
            print(get_memory_info())
            print()
            print(get_disk_info())
            print()
            net_str, net_prev = get_network_info(net_prev)
            print(net_str)
            time.sleep(5)
            if args.once:
                break

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
