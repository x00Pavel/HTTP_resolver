SERV = serv.py
RED=\033[0;31m
YELLOW=\033[1;33m
BLUE=\033[1;34m
NC=\033[0m # No Color

build:
	@echo 'Done'

run:
ifdef PORT
	python3 ${SERV} ${PORT}
else
	@echo '${RED}No port specified${NC}'
endif
 
get:
ifdef PORT
	@echo -e '\n${YELLOW}Test GET request${NC}'
	@echo '---------------------------------'
	curl -v localhost:${PORT}/resolve?name=www.fit.vutbr.cz\&type=A
	@echo '---------------------------------'
	curl -v localhost:${PORT}/resolve?name=46.255.231.42\&type=PTR
	@echo '---------------------------------'
	curl -v localhost:${PORT}/reslve?name=46.255.231.42\&type=PTR
	@echo '---------------------------------'
	curl -v localhost:${PORT}/resolve?name=46255.231.42\&type=PTR
	@echo '---------------------------------'
	curl -v localhost:${PORT}/resolve?name=www.fit.vutbr.cz\&type=PTa
	@echo '---------------------------------'
	curl -v localhost:${PORT}/reolve?name=www.fit.vutbr.cz\&type=PTR
	@echo '---------------------------------'
	curl -v localhost:${PORT}/resolve?name=www-us.computershare.com\&type=PTR
	@echo '---------------------------------'
	curl -v localhost:${PORT}/resolve?name=g.cn\&type=PTR
	@echo '---------------------------------'
	curl -v localhost:${PORT}/resolve?name=g.cn\&type=A
	@echo -e '${YELLOW}Test GET request completed${NC}\n'
	
else
	@echo -e '${RED}No port specified${NC}'
endif

post:
ifdef PORT
	@echo -e '\n${YELLOW}Test POST request${NC}'
	curl -v --data-binary @queries.txt -X POST http://localhost:${PORT}/dns-query
	@echo '---------------------------------'
	curl -v --data-binary @links_1.txt -X POST http://localhost:${PORT}/dns-query
	@echo '---------------------------------'
	curl -v --data-binary @qwe -X POST http://localhost:${PORT}/dns-query
	@echo -e '${YELLOW}Test POST request completed${NC}\n'

else
	@echo -e '${RED}No port specified${NC}'
endif
clean:
	lsof -i :1234
	
listen:
	netstat -an | grep -G :1234
zip:
	zip -r xyadlo00.zip Makfile src/ readme.md

wget_get:
	wget -vO- "localhost:1234/resolve?name=www.fit.vutbr.cz&type=A"
	wget -vO- "localhost:1234/resolve?name=www.fit.vutbr.cz&type=PTR" 

wget_post:
	wget -vO- --post-file=queries.txt http://localhost:${PORT}/dns-query