import socket
import json

packet = {
    'seq_no':0,
    'ack_no':0,
    'flags':{
        'U': 0,
        'A': 0,
        'P': 0,
        'R': 0,
        'S': 0,
        'F': 0
    },
    'data':''
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

def set_packet(seq_no, ack_no, flags, data):
    packet['seq_no'] = seq_no
    packet['ack_no'] = ack_no
    flags = flags.split(' ')
    for flag in flags:
        packet['flags'][flag] = 1
    data = ''

def connection_establisment():
    print('Listening')
    msg = json.loads(client_socket.recv(1024).decode('ascii'))
    if(msg['flags']['S'] == 1):
        set_packet(1000, 0, 'S A', '')
        client_socket.send(json.dumps(packet).encode('ascii'))
        reset_packet()
        print('SYN RECVD')
    msg = json.loads(client_socket.recv(1024).decode('ascii'))
    if(msg['flags']['A'] == 1):
        print('ESTABLISHED')

def connection_termination_three_way():
    msg = json.loads(client_socket.recv(1024).decode('ascii'))
    if(msg['flags']['F'] == 1):
        print('CLOSE WAIT')
        set_packet(1000, 0, 'F A', '')
        client_socket.send(json.dumps(packet).encode('ascii'))
        reset_packet()
        print('LAST ACK')
        msg = json.loads(client_socket.recv(1024).decode('ascii'))
        if(msg['flags']['A'] == 1):
            print('CLOSED')

if __name__ == "__main__":
    server_socket = socket.socket()
    server_socket.bind(('', 9999))
    server_socket.listen(1)
    client_socket, addr = server_socket.accept()
    connection_establisment()
    connection_termination_three_way()
