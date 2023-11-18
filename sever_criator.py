import socket
import random
import json
import time

abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


logins_list = [
    'admin', 'Admin', 'admin1', 'admin2', 'admin3',
    'user1', 'user2', 'root', 'default', 'new_user',
    'some_user', 'new_admin', 'administrator',
    'Administrator', 'superuser', 'super', 'su', 'alex',
    'suser', 'rootuser', 'adminadmin', 'useruser',
    'superadmin', 'username', 'username1'
]


def logins():
    for login in logins_list:
        yield login


def random_login():
    return random.choice(list(logins()))


def random_password():
    '''function - generating random password of length from 6 to 10'''
    return ''.join(random.choice(abc) for i in range(random.randint(6, 10)))


def server(server_login, server_password):
    HOST = '127.0.0.1'
    PORT = 9090
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        try:
            s.listen(1)
            print("waiting for new connection")
            print(server_login)
            print(server_password)
            conn, addr = s.accept()
            time.sleep(4)
            print("connection established ")
            with conn:
                while True:
                    data = conn.recv(1024)

                    try:
                        login_ = json.loads(data.decode('utf8'))['login']
                        password_ = json.loads(data.decode('utf8'))['password']
                    except:
                        conn.send(json.dumps({'result': 'Bad request!'}).encode('utf8'))
                        continue

                    if login_ == server_login:

                        if server_password == password_:
                            conn.send(
                                json.dumps({
                                    'result': 'Connection success!'
                                }).encode('utf8'))
                            break
                        elif server_password.startswith(password_):
                            delay = 0.1  # initial delay time
                            while True:
                                time.sleep(delay)  # wait for delay time
                                new_password = password_ + random.choice(abc)
                                conn.send(json.dumps({'login': login_, 'password': new_password}).encode('utf8'))
                                start = time.time()  # start timer
                                response = conn.recv(1024)
                                end = time.time()  # end timer
                                if (end - start) >= delay:  # if delay time has passed
                                    password_ = new_password  # update the password
                                    delay = 0.1  # reset the delay time
                                    if json.loads(response.decode('utf8'))['result'] == 'Connection success!':
                                        conn.send(json.dumps({'login': login_, 'password': new_password}).encode('utf8'))
                                        break
                                else:
                                    delay *= 2  # double the delay time for next iteration
                        else:
                            conn.send(
                                json.dumps({
                                    'result': 'Wrong password!'
                                }).encode('utf8'))
                    else:
                        conn.send(json.dumps({'result': 'Wrong login!'}).encode('utf8'))
        except:
            pass


server(random_login(), random_password())
