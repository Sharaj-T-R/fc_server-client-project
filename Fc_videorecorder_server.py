import numpy as np
import cv2
import paramiko
import imagiz
from datetime import datetime
from guizero import App, Text, PushButton
from PIL import Image


def nothing(int):
    pass


def initiate_con():
    hostname1 = "192.168.0.101"
    hostname2 = "192.168.0.104"
    hostname3 = "192.168.0.105"
    hostname4 = "192.168.0.106"
    username = "pi"
    password = "NDL"
    client1 = paramiko.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client2 = paramiko.SSHClient()
    client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client3 = paramiko.SSHClient()
    client3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client4 = paramiko.SSHClient()
    client4.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client1.connect(hostname=hostname1, username=username, password=password)
        client2.connect(hostname=hostname2, username=username, password=password)
        client3.connect(hostname=hostname3, username=username, password=password)
        client4.connect(hostname=hostname4, username=username, password=password)


    except:
        print("[!] Cannot connect to the SSH Server")
        exit()
    bash_script = open("bash.txt").read()
    stdin1, stdout1, stderr1 = client1.exec_command(bash_script)
    stdin2, stdout2, stderr2 = client2.exec_command(bash_script)
    stdin3, stdout3, stderr3 = client3.exec_command(bash_script)
    stdin4, stdout4, stderr4 = client4.exec_command(bash_script)
    print(stdout1.read().decode())
    print(stdout2.read().decode())
    print(stdout3.read().decode())
    print(stdout4.read().decode())
    err1 = stderr1.read().decode()
    if err1:
        print(err1)
    client1.close()
    err2 = stderr1.read().decode()
    if err2:
        print(err2)
    client2.close()
    err3 = stderr3.read().decode()
    if err3:
        print(err3)
    client3.close()
    err4 = stderr4.read().decode()
    if err4:
        print(err4)
    client4.close()
    return


def connect():
    i = 0
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_cham1 = cv2.VideoWriter('chamber_1.mp4', fourcc, 30.0, (640, 480))
    out_cham2 = cv2.VideoWriter('chamber_2.mp4', fourcc, 30.0, (640, 480))
    out_cham3 = cv2.VideoWriter('chamber_3.mp4', fourcc, 30.0, (640, 480))
    out_cham4 = cv2.VideoWriter('chamber_4.mp4', fourcc, 30.0, (640, 480))
    sock_receiver_cham1 = imagiz.TCP_Server(9999)
    sock_receiver_cham2 = imagiz.TCP_Server(8888)
    sock_receiver_cham3 = imagiz.TCP_Server(8899)
    sock_receiver_cham4 = imagiz.TCP_Server(9988)
    sock_receiver_cham1.start()
    sock_receiver_cham2.start()
    sock_receiver_cham3.start()
    sock_receiver_cham4.start()
    f = open('time_stamp', 'w+b')
    cv2.namedWindow('Fc_recorder', cv2.WINDOW_NORMAL)
    switch = '0 : pre \n 1 : ON \n 2 : OFF'
    cv2.createTrackbar(switch, 'Fc_recorder', 0, 2, nothing)
    message = sock_receiver_cham1.receive()
    ima = cv2.imdecode(message.image, 1)
    (h, w) = ima.shape[:2]
    cv2.resizeWindow('Fc_recorder', 640, 480)
    output = np.zeros((h * 2, w * 2, 3), dtype="uint8")
    while True:
        message1 = sock_receiver_cham1.receive()
        message2 = sock_receiver_cham2.receive()
        message3 = sock_receiver_cham3.receive()
        message4 = sock_receiver_cham4.receive()
        image1 = cv2.imdecode(message1.image, 1)
        image2 = cv2.imdecode(message2.image, 1)
        image3 = cv2.imdecode(message3.image, 1)
        image4 = cv2.imdecode(message4.image, 1)
        output[0:h, 0:w] = image1
        output[0:h, w:w * 2] = image2
        output[h:h * 2, w:w * 2] = image1
        output[h:h * 2, 0:w] = image2
        cv2.imshow('Fc_recorder', output)
        s = cv2.getTrackbarPos(switch, 'Fc_recorder')
        cv2.waitKey(1)
        if s == 1:
            i = 1
        if i == 1:
            date_time = str(datetime.now())
            byt = date_time.encode('utf-8')
            f.write(byt)
            out_cham1.write(image1)
            out_cham2.write(image2)
            out_cham3.write(image3)
            out_cham4.write(image4)
        if s == 2:
            i = 0
            break
    f.close()
    out_cham1.release()
    out_cham2.release()
    out_cham3.release()
    out_cham4.release()
    cv2.destroyAllWindows()
    return


app1 = App(title="FC-video-recorder")
intro = Text(app1, text="Click connect to establish connections with all chambers.")
start = PushButton(app1, command=connect, text="connect to all chambers")
initiate_connection = PushButton(app1, command=initiate_con, text="initiate pi cam")

app1.display()
