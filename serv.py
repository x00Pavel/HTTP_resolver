import socket
import re
import sys

delim = "-"
ok_200 = "HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n".encode('utf-8')
bad_400 = "HTTP/1.1 400 Bad Request\r\nConnection: close\r\n\r\n".encode(
    'utf-8')
bad_404 = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n".encode('utf-8')
bad_405 = " HTTP/1.1 405 Method Not Allowed\r\nConnection: close\r\n\r\n".encode(
    'utf-8')
serverPort = sys.argv[1] if sys.argv[1] else 123456

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("Socket create: success")

serverSocket.bind(('', int(serverPort)))
print("Socket bind: success")

serverSocket.listen(5)
print("Socket listining: Ready\n" + delim *
      len("Socket listining: Ready") + "\n")

tip_arr = ['A', 'PTR']
tip = ''
name = ''


def output(text, answer=None):
    print("\n"+delim*len(text))
    print(text)
    if(answer != None):
        print(answer)
    print(delim*len(text)+"\n")


def get_req(data):
    output("Request is:", data)
    try:
        first_line = data.split("\r\n")[0]
        if not re.match(r'^GET \/resolve\?name=[1-z0-9A-Z\.\-]*&type=(PTR|A) HTTP\/1\.1$', first_line):
            print("Wrong first line")
            return bad_400
        tip = re.findall(r'(A|PTR)', first_line)
    except:
        print("Not type specified. Closed")
        return(bad_400)

    if (not tip):
        output("400 Bad Type of request")
        return(bad_400)

    try:
        try:
            name = data.split("/resolve?name=")[1].split("&")[0]
            reg = re.compile(
                r"""(^((1?[0-9]?[0-9]\.)|
                       (2[0-4]?[0-9]\.)|
                       (25[0-5]?\.)){3}((1?[0-9]?[0-9])|
                       (2[0-4]?[0-9])|(25[0-5]?))$)|
                       (^[a-z\-]{0,6}\.?[a-zA-Z1-9]{1,}[a-zA-Z1-9\-]*\.[a-z]{2,5}$)
                       """, re.VERBOSE)
            if not re.match(reg, name):
                print (f"NOT MATCH: {name}")
                return bad_400
        except:
            return bad_400
        addr = ''
        tip = tip[0]
        if(tip == "A"):
            addr = socket.gethostbyname(name)
        elif (tip == "PTR"):
            addr = socket.gethostbyaddr(name)[0]
        else:
            print("405 Bad Type of request: {}".format(tip))
            return(bad_405)
        if not addr:
            output("404 Not Found")
            return bad_404
        else: 
            output("Answer of GET request is:", "{}:{}={}".format(name, tip, addr))
            return(ok_200 + "{}:{}={}\n".format(name, tip, addr).encode('utf-8'))
    except:
        return(bad_404)


def post_req(data):
    first_line = data.split("\r\n")[0]
    if first_line !=  "POST /dns-query HTTP/1.1":
        print("wrong first line")
        return bad_400
    query = data.split("\r\n\r\n")[1]
    output("Body of POST request:", query)

    links = list(query.split("\n"))
    query_dict = {}
    for link in links:
        try:
            host_name, tip = link.split(":")
            if tip not in tip_arr:
                continue
            query_dict[host_name] = tip
        except:
            print("wrong format: {}".format(link))
            continue
            # return bad_400
    answer = ''

    for host, tip in query_dict.items():
        try:
            addr = ''
            if(tip == "A"):
                addr = socket.gethostbyname(host)
            elif (tip == "PTR"):
                addr = socket.gethostbyaddr(host)[0]
            else:
                print(f"Bad type {tip}")
                continue
            if addr:
                answer = answer + f'{host}:{tip}={addr}\n'
        except:
            print("400 Bad Request with addr: {}".format(host))
            continue
            # return bad_400
    output("Answer of POST request is:", answer)
    return ok_200 + answer.encode('utf-8')


# Main loop
while True:
    # accept connections from outside
    cl_socket, address = serverSocket.accept()
    data = cl_socket.recv(1024)

    output("Got a connection from {}".format(str(address)))

    data = data.decode('utf-8')
    req_type = data.split(" ")[0]
    if(req_type == 'GET'):
        cl_socket.send(get_req(data))
    elif(req_type == 'POST'):
        cl_socket.send(post_req(data))
    else:
        cl_socket.send(bad_405)

    cl_socket.close()

serverSocket.shutdown(socket.SHUT_RDWR)
serverSocket.close()
print("Connection closed")
sys.exit(1)
