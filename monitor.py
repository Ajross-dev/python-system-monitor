# collects and saves system metrics

import os
import time
import psutil

from logger import save_metrics

REFRESH_SECONDS = 25


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def bytes_to_gb(bytes_value):
    return round(bytes_value / (1024 ** 3), 2)


def get_metrics():
    """Collects CPU, memory, disk, and network data"""
    cpu_usage = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()
    memory_percent = memory.percent

    disk = psutil.disk_usage("/")
    disk_percent = disk.percent

    network = psutil.net_io_counters()
    bytes_sent = network.bytes_sent
    bytes_received = network.bytes_recv

    return cpu_usage, memory_percent, disk_percent, bytes_sent, bytes_received


def show_cpu(cpu_usage):
    cpu_count = psutil.cpu_count()

    print("CPU")
    print(f"Usage: {cpu_usage}%")
    print(f"Cores: {cpu_count}")
    print()


def show_memory(memory_percent):
    memory = psutil.virtual_memory()

    used_gb = bytes_to_gb(memory.used)
    total_gb = bytes_to_gb(memory.total)

    print("Memory")
    print(f"Used: {used_gb} GB / {total_gb} GB")
    print(f"Percent Used: {memory_percent}%")
    print()


def show_disk(disk_percent):
    disk = psutil.disk_usage("/")

    used_gb = bytes_to_gb(disk.used)
    total_gb = bytes_to_gb(disk.total)

    print("Disk")
    print(f"Used: {used_gb} GB / {total_gb} GB")
    print(f"Percent Used: {disk_percent}%")
    print()


def show_network(bytes_sent, bytes_received):
    """Displays total network data sent and received"""
    sent_mb = round(bytes_sent / (1024 ** 2), 2)
    received_mb = round(bytes_received / (1024 ** 2), 2)

    print("Network")
    print(f"Data Sent: {sent_mb} MB")
    print(f"Data Received: {received_mb} MB")
    print()


def main():
    while True:
        clear_screen()

        cpu, memory, disk, sent, received = get_metrics()

        save_metrics(cpu, memory, disk, sent, received)

        print("System Monitor Running...")
        print("Press Ctrl+C to stop")
        print()

        show_cpu(cpu)
        show_memory(memory)
        show_disk(disk)
        show_network(sent, received)

        print("Metrics saved.")

        time.sleep(REFRESH_SECONDS)


if __name__ == "__main__":
    main()