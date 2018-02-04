SHELL=/bin/bash

all:
	@# install required dependencies
	virtualenv env
	source env/bin/activate
	env/bin/pip install -r requirements.txt

clean:
	@find . -name "*.pyc" -exec rm {} \; 

fullclean:
	@find . -name "*.pyc" -exec rm {} \; 
	@rm -r env
