#!/usr/bin/python

import flask, binascii, socket, struct, sys, time
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

endpoint_ip='127.0.0.1'
endpoint_port='127'
result = ""

def server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_server_address = (endpoint_ip, endpoint_port)
    sock.bind(receiver_server_address)
    sock.listen(1)

    unpacker = struct.Struct('10s')

    while True:
        print >>sys.stderr, '\nwaiting for a connection'
        connection, client_address = sock.accept()
        try:
            data = connection.recv(unpacker.size)
            print >>sys.stderr, 'received "%s"' % binascii.hexlify(data)

            unpacked_data = unpacker.unpack(data)
            result = unpacked_data
            print >>sys.stderr, 'unpacked:', unpacked_data
            
        finally:
            connection.close()

def client(cmd):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endpoint_address = (endpoint_ip, endpoint_port)
    sock.connect(endpoint_address)

    values = cmd
    packer = struct.Struct('10s')
    packed_data = packer.pack(*values)

    try:
        # Send data
        print >>sys.stderr, 'sending "%s"' % binascii.hexlify(packed_data), values
        sock.sendall(packed_data)
    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()


@app.route('/', methods=['GET'])
def home():
    return '''<h5>API endpoint:</h5>
<p>[GET] /api/v1/command    --  get all events</p>
<p>Sample: curl http://192.168.12.34/api/v1/command?cmd=7e0433ab2112ab0e</p>'''

@app.route('/api/v1/command', methods=['GET'])
def api_all():
    cmd = event['queryStringParameters']['cmd']
    client(cmd)
    time.sleep(2.1)
    server()
    return {
        'statusCode': 200,
        'body': result
    }



app.run()
