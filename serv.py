import socket
import re
import sys

delim = "-"

serverPort = sys.argv[1] if sys.argv[1] else 123456

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket create: success")

serverSocket.bind(('', int(serverPort)))
print("Socket bind: success")

serverSocket.listen(2)
print("Socket listining: Ready\n" + delim *
      len("Socket listining: Ready") + "\n")

tip_arr = ['A', 'PTR']
tip = ''
name = ''

def output(text, answer=None):
    print(delim*len(text))
    print(text)
    if(answer != None):
        print(answer)
    print(delim*len(text))


def get_req(data):
    output("Request is:", data)
    tip = data.split("&type=")[1].split(" ")[0]
    if (tip not in tip_arr):
        print("400 Bad Type of request: {}".format(tip))
        return("400 Bad Request\n".encode('utf-8'))

    try:
        name = data.split("/resolve?name=")[1].split("&")[0]
        addr = ''
        if(tip == "A"):
            addr = socket.gethostbyname(name)
        elif (tip == "PTR"):
            if (re.findall(r'[a-zA-Z]+', name)):
                print("Wrong name, should be IP addres, but you have: {}".format(name))
                return("400 Bad Request\n".encode('utf-8'))
            addr = socket.gethostbyaddr(name)[0]
        else:
            print("400 Bad Type of request: {}".format(tip))
            return("400 Bad Request\n".encode('utf-8'))
        output("Answer of GET request is:", "{}:{}={}".format(name, tip, addr))
        return("{}:{}={}\n".format(name, tip, addr).encode('utf-8'))
    except:
        return("400 Bad Request\n".encode('utf-8'))


def post_req(data):
    query = data.split("\r\n\r\n")[1]
    output("Body of POST request:", query)

    links = list(query.split("\n"))
    query_dict = {}
    for link in links:
        try:
            host_name, tip = link.split(":")
            query_dict[host_name] = tip
        except:
            print("wrong format: {}".format(link))
    answer = ''
    for host, tip in query_dict.items():
        try:
            addr = ''
            if(tip == "A"):
                addr = socket.gethostbyname(host)
            elif (tip == "PTR"):
                addr = socket.gethostbyaddr(host)[0]
            else:
                print(f"Bad type {tip}\n")
                continue
            answer = answer + f'{host}:{tip}={addr}\n'
        except:
            print("400 Bad Request with addr: {}\n".format(host))
    output("Answer of POST request is:", answer)
    return answer.encode('utf-8')

# Main loop
while True:
    # accept connections from outside
    cl_socket, address = serverSocket.accept()
    data = cl_socket.recv(1024)

    output("Got a connection from {}".format(str(address)))

    data = data.decode('utf-8')
    # print(data + '\n')
    req_type = data.split(" ")[0]
    if(req_type == 'GET'):
        cl_socket.send(get_req(data))
    elif(req_type == 'POST'):
        cl_socket.send(post_req(data))
    else:
        cl_socket.send("400 Bad Request\n".encode('utf-8'))

    cl_socket.close()
