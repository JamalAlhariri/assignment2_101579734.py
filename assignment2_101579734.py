"""
Author: Jamal Alhariri
Assignment: #2
Description: Port Scanner — A tool that scans a target machine for open network ports
"""

import socket
import threading
import sqlite3
import os
import platform
import datetime

print("Python Version:", platform.python_version())
print("Operating System:", os.name)

#  stores port numbers and service names
common_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt"
}


class NetworkTool:
    def __init__(self, target):
        self.__target = target

    # Q3: What is the benefit of using @property and @target.setter?
    # It lets the program control how the target is used and changed.
    # This is better than changing the variable directly because it can check for bad values first.
    # In this case it stops the target from being set to an empty string.

    
    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        if value != "":
            self.__target = value
        else:
            print("Error: Target cannot be empty")
    def __del__(self):
        print("NetworkTool instance destroyed")


# Q1: How does PortScanner reuse code from NetworkTool?
# PortScanner reuses code by inheriting from NetworkTool.
# It gets the target variable and the getter and setter from the parent class.
# For example, PortScanner can use self.target without making that code again.



class PortScanner(NetworkTool):
    def __init__(self, target):
        super().__init__(target)
        self.scan_results = []
        self.lock = threading.Lock()
    def __del__(self):
        print("PortScanner instance destroyed")
        super().__del__()
    def scan_port(self, port):
        sock = None


        # Q4: What would happen without try-except here?
        # Without try-except, a socket error could stop the whole program.
        # If the machine could not be reached, the scan might crash before finishing the rest of the ports.
        # This makes the program safer and allows it to keep going.



        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                status = "Open"
            else:
                status = "Closed"
            service_name = common_ports.get(port, "Unknown")
            self.lock.acquire()
            self.scan_results.append((port, status, service_name))
            self.lock.release()

        except socket.error as e:
            print(f"Error scanning port {port}: {e}")

        finally:
            if sock:
                sock.close()
    def get_open_ports(self):
        return [item for item in self.scan_results if item[1] == "Open"]



    # Q2: Why do we use threading instead of scanning one port at a time?
    # Threading helps scan many ports faster because more than one port can be checked at once.
    # If 1024 ports were scanned one by one, it would take a lot longer.
    # Using threads makes the scanner more efficient.



    def scan_range(self, start_port, end_port):
        threads = []
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()



def save_results(target, results):
    try:
        conn = sqlite3.connect("scan_history.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            port INTEGER,
            status TEXT,
            service TEXT,
            scan_date TEXT
        )
        """)

        for result in results:
            port = result[0]
            status = result[1]
            service = result[2]

            cursor.execute("""
            INSERT INTO scans (target, port, status, service, scan_date)
            VALUES (?, ?, ?, ?, ?)
            """, (target, port, status, service, str(datetime.datetime.now())))

        conn.commit()
        conn.close()

    except sqlite3.Error:
        print("Database error")


def load_past_scans():
    try:
        conn = sqlite3.connect("scan_history.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM scans")
        rows = cursor.fetchall()

        for row in rows:
            print(f"[{row[5]}] {row[1]} : Port {row[2]} ({row[4]}) - {row[3]}")
        conn.close()
    except sqlite3.Error:
        print("No past scans found.")




if __name__ == "__main__":
    try:
        target = input("Enter target IP (default 127.0.0.1): ")
        if target == "":
            target = "127.0.0.1"

        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))

        if start_port < 1 or end_port > 1024:
            print("Port must be between 1 and 1024.")
        elif end_port < start_port:
            print("Port must be between 1 and 1024.")
        else:
            scanner = PortScanner(target)

            print("Scanning...")

            scanner.scan_range(start_port, end_port)

            open_ports = scanner.get_open_ports()

            for p in open_ports:
                print(p)

            print("Total open ports:", len(open_ports))

            save_results(target, scanner.scan_results)

            choice = input("See past scans? ")
            if choice.lower() == "yes":
                load_past_scans()

    except:
        print("Invalid input.")




# Q5: New Feature Proposal
# One feature I would want to add is to group the ports by their services.
# This could be done by only using open ports and grouping them based on the service name from the common_ports dictionary with a list comprehension.
# It would make it easier to understand what kinds of services are running on the target instead of just seeing individual ports.
# Diagram: See diagram_101579734.png in the repository root