# IPK 1 project - HTTP resolver doménových jmen

## Author: Pavel Yadlosuki (_xyadlo00_)  

## Date: 02.2020

### Abstract

Aim of this project is to implement HTTP server which will be support basic requests such as GET and POST. Client send to server GET or POST requests in specific format

### Implementation

Main body of program is represented as finite while loop. Inside this loop processing of all request is held. In case of unsupported operation server will send to user reply "405 Bad Type of request

1) **_get_req_** for processing GET request
2) **_post_req_** for processing POST request

In each function parsing is held based on specified format of current request.

For GET request parser try to extract URL or IP address from header. Also during extraction it checks lexical elements of request. For example GET request must contain of in header such sting

> GET /resolve?name=<ADDR\>&type=<TYPE\> HTTP/1.1

where <ADDR\> is URL or IP address and <TYPE\> is type of expected response in following format:
[req]: get
> <ADDR\>:<TYPE\>=<ANSWER\>

where <ANSWER\> is corresponding answer (host name or IP address) to given <ADDR\> and <TYPE\>. In success corresponding response is send with code "200 Ok". In case if request is in wrong format, response would be "400 Bad Request".

For POST request there is must be specified file, where would be on each line written address and type of expecting answer in following format:

> <ADDR\>:<TYPE\>

Empty line is skipped. __[[TODO]] WHAT WOULD BE IF THERE WOULD BE WRONG FORMAT__

In success response contain code "200 Ok" and answers in format like in GET request, but there are on each line answer on each correct request from given file.
In error, server send response with code "400 Bad Request"
