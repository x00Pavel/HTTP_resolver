NO_COLOR=\033[0m'
TEST_COLOR='\033[93m
OK_COLOR='\033[92m
ERROR_COLOR='\033[91m

help:
	@echo 'Commands:'
	@echo '$}make run PORT=`0-65535`'
	@echo '$}make test PORT=`0-65535` qv=`q` or `v`'
	@echo '$}make zip'
zip:
	zip -r xabram00.zip readme.md Makefile src	

run:
ifdef PORT
	python3 src/server.py $(PORT)
else
	@echo 'please, define: PORT=int (0-65535)'
endif

test: 
ifdef PORT
ifeq ($(qv),$(filter $(qv),v q))
	@echo -e $(TEST_COLOR)CURL TESTS STARTED$(NO_COLOR)
	@echo -e $(ERROR_COLOR)Error 405: CURL PUT TEST (nothing) $(NO_COLOR)
	curl -$(qv)X PUT -d 'name=mkyong&email=abc@gmail.com' http://localhost:$(PORT) || true
	@echo -e $(ERROR_COLOR)Error 404: CURL GET TEST (nothing) $(NO_COLOR)
	curl -$(qv) localhost:$(PORT)/resolve?name=223.255.255.255\&type=A || true
	@echo -e $(ERROR_COLOR)Error 400: CURL GET TEST (nothing) $(NO_COLOR)
	curl -$(qv) localhost:$(PORT)/resolve?name=www.fit.vutbr.cz\&type=PTRfsf || true
	@echo -e $(ERROR_COLOR)Error 400: CURL POST TEST (nothing) $(NO_COLOR)
	curl -$(qv) --data-binary @src/tests/test3 -X POST http://localhost:$(PORT)/dns-query || true
	@echo -e $(OK_COLOR)CURL GET TEST$(NO_COLOR)
	curl -$(qv) localhost:$(PORT)/resolve?name=www.fit.vutbr.cz\&type=A || true
	@echo -e $(OK_COLOR)CURL POST TEST$(NO_COLOR)
	curl -$(qv) --data-binary @src/tests/test1 -X POST http://localhost:$(PORT)/dns-query || true
	@echo -e $(TEST_COLOR)CURL TESTS FINISHED$(NO_COLOR)
	@echo -e $(TEST_COLOR)WGET TESTS STARTED$(NO_COLOR)
	@echo -e $(ERROR_COLOR)Error 405: WGET HEAD TEST (nothing) $(NO_COLOR)
	wget -$(qv)O- --spider localhost:$(PORT) || true
	@echo -e $(ERROR_COLOR)Error 404: WGET GET TEST (nothing) $(NO_COLOR)
	wget -$(qv)O- "localhost:$(PORT)/resolve?name=147.229.14.11&type=PTR" || true
	@echo -e $(ERROR_COLOR)Error 400: WGET GET TEST (nothing) $(NO_COLOR)
	wget -$(qv)O- "localhost:$(PORT)/resolve?name=www.fit.vutbr.cz&type=PTRfsf" || true
	@echo -e $(ERROR_COLOR)Error 400: WGET POST TEST (nothing) $(NO_COLOR) 
	wget -$(qv)O- --post-file=src/tests/test3 http://localhost:$(PORT)/dns-query || true
	@echo -e $(OK_COLOR)WGET GET TEST$(NO_COLOR)
	wget -$(qv)O- "localhost:$(PORT)/resolve?name=www.fit.vutbr.cz&type=A" || true
	@echo -e $(OK_COLOR)WGET POST TEST$(NO_COLOR)
	wget -$(qv)O- --post-file=src/tests/test1 http://localhost:$(PORT)/dns-query || true
	@echo -e $(TEST_COLOR)WGET TESTS FINISHED$(NO_COLOR)
else
	@echo 'please, define: make test PORT=`0-65535` qv=`q` or `v`'
endif
endif