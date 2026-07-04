# Simple System Monitor using psutil
# Run: python monitor.py

import os
import time
import psutil


REFRESH_SECONDS = 2


def clear_screen():
    """Clears the terminal screen."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def bytes_to_gb(bytes_value):
    """Converts bytes into gigabytes."""
    return round(bytes_value / (1024 ** 3), 2)


def show_cpu():
    """Displays CPU usage."""
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()

    print("CPU")
    print(f"Usage: {cpu_usage}%")
    print(f"Cores: {cpu_count}")
    print()


def show_memory():
    """Displays RAM usage."""
    memory = psutil.virtual_memory()

    used_gb = bytes_to_gb(memory.used)
    total_gb = bytes_to_gb(memory.total)

    print("Memory")
    print(f"Used: {used_gb} GB / {total_gb} GB")
    print(f"Percent Used: {memory.percent}%")
    print()


def show_disk():
    """Displays disk usage."""
    disk = psutil.disk_usage("/")

    used_gb = bytes_to_gb(disk.used)
    total_gb = bytes_to_gb(disk.total)

    print("Disk")
    print(f"Used: {used_gb} GB / {total_gb} GB")
    print(f"Percent Used: {disk.percent}%")
    print()


def show_network():
    """Displays total network data sent and received."""
    network = psutil.net_io_counters()

    sent_mb = round(network.bytes_sent / (1024 ** 2), 2)
    received_mb = round(network.bytes_recv / (1024 ** 2), 2)

    print("Network")
    print(f"Data Sent: {sent_mb} MB")
    print(f"Data Received: {received_mb} MB")
    print()


def main():
    """Main program loop."""
    while True:
        clear_screen()

        print("=== Simple System Monitor ===")
        print("Press Ctrl+C to stop")
        print()

        show_cpu()
        show_memory()
        show_disk()
        show_network()

        time.sleep(REFRESH_SECONDS)


if __name__ == "__main__":
    main()
