import socket
import json
import time
packet = {
    'seq_no': 0,
    'ack_no': 0,
    'flags': {
        'U': 0,
        'A': 0,
        'P': 0,
        'R': 0,
        'S': 0,
        'F': 0
    },
    'data': ''
}

def reset_packet():
    packet['seq_no'] = 0
    packet['ack_no'] = 0
    packet['data'] = ''
    packet['flags']['U'] = 0
    packet['flags']['A'] = 0
    packet['flags']['P'] = 0
    packet['flags']['R'] = 0
    packet['flags']['S'] = 0
    packet['flags']['F'] = 0


def set_packet(seq_no,ack_no,flags,data):
    packet['seq_no'] = seq_no
    packet['ack_no'] = ack_no
    flags = flags.split(' ')
    for flag in flags:
        packet['flags'][flag] = 1
    data = ''

def connection_establisment():
    set_packet(8000,0,'S','')
    client_socket.send(json.dumps(packet).encode('ascii'))
    reset_packet()
    print('SYN SENT')
    msg = json.loads(client_socket.recv(1024).decode('ascii'))
    if(msg['flags']['S'] == 1 and msg['flags']['A'] == 1):
        set_packet(8000, 0, 'A', '')
        client_socket.send(json.dumps(packet).encode('ascii'))
        reset_packet()
        print('ESTABLISHED')


def connection_termination_three_way():
    set_packet(8000, 0, 'F', '')
    client_socket.send(json.dumps(packet).encode('ascii'))
    reset_packet()
    print('FIN WAIT 1')
    msg = json.loads(client_socket.recv(1024).decode('ascii'))
    if(msg['flags']['F'] == 1 and msg['flags']['A'] == 1):
        print('TIME WAIT')
        set_packet(8000, 0, 'A', '')
        client_socket.send(json.dumps(packet).encode('ascii'))
        reset_packet()
        time.sleep(2)
        print('CLOSED')

if __name__ == "__main__":
    client_socket = socket.socket()
    client_socket.connect(('localhost',9999))
    connection_establisment()
    connection_termination_three_way()
