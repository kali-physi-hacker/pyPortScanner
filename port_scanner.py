import socket 
from queue import Queue 
import threading
import argparse
from datetime import datetime

from utils import SmartDescriptionFormatter


# TODO: Implement option to add port range like -pr or --port-range (for port ranges)


PORT_QUEUE = Queue()
OPEN_PORTS = []
THREAD_LIST = []
THREAD_NUM = 10


def scan_port(target, port):
    """
    Return True if port is reachable; Return False otherwise.
    :param target:
    :param port:
    :return:
    """
    try:
        socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_object.connect((target, port))
        return True
    except:
        return False


def populate_queue(ports):
    """
    Fill PORT_QUEUE with port_list.
    :param ports:
    :return:
    """
    for port in ports:
        PORT_QUEUE.put(port)


def worker(port_queue, target):
    """
    Thread function that scans port and appends opened ports to OPEN_PORTS list.
    :return:
    """
    while not port_queue.empty():
        port = port_queue.get()
        if scan_port(target, port):
            OPEN_PORTS.append(port)
            print(f"\tPort {port} is Opened")
        # else:
        #     print(f"Port {port} is Closed")


def construct_threads(thread_number, port_queue, target):
    """
    Create thread objects and append them to the THREAD_LIST
    :param thread_number:
    :return:
    """
    for t_index in range(thread_number):
        thread = threading.Thread(target=worker, args=(port_queue, target))
        THREAD_LIST.append(thread)


def run_threads():
    """
    Execute all the threads.
    :return:
    """
    for thread in THREAD_LIST:
        thread.start()


def finalize_execution():
    """
    Pause code execution until threads are completed
    :return:
    """
    for thread in THREAD_LIST:
        thread.join()



def main():
    """
    Execute program
    """
    parser = argparse.ArgumentParser(
        description="""
        Script for performing port scanning on a specified target / host.
        Example Usage:
            1. python port_scanner.py                       -           Scans port on ip/host => localhost, thread => 10
            2. python port_scanner.py -ip 192.168.12.1 100   -           Scans port on ip/host => 192.168.12.1 thread => 100
        """,
        formatter_class=SmartDescriptionFormatter
    )
    parser.add_argument("-ip", "--host", help="Specify the target host (default => localhost)")
    parser.add_argument("-t", "--thread", help="Specify the number of threads to use for the connections (default => 10)", type=int)
    options = parser.parse_args()

    ports = range(1, 65211)
    thread_number = options.thread or THREAD_NUM
    host = options.host or 'localhost'

    print(f"""
    Port Scanning Started {datetime.now()}
    -----------------------------------------------------------
    Target Host => {host}
    Threads => {thread_number}

    """)

    start_time = datetime.now()

    populate_queue(ports)
    construct_threads(thread_number, PORT_QUEUE, host)
    run_threads()
    finalize_execution()

    end_time = datetime.now()
    delta_time = end_time - start_time

    print(f"""
    Port Scanning Done in {delta_time}
    -----------------------------------

    Open Ports:
    {OPEN_PORTS}
    """)


if __name__ == "__main__":
    main()