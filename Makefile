FUNCTION_NAME=RSSReader
STACK_NAME=Lambda$(FUNCTION_NAME)
PROFILE=

.PHONY: zip
zip: clean
	@pip install --upgrade feedparser -t . > /dev/null
	@zip -r function lambda_function.py feedparser.py > /dev/null

.PHONY: clean
clean:
	@rm -f function.zip

.PHONY: create
create: zip
	unset AWS_DEFAULT_REGION; \
	aws configure --profile $(PROFILE); \
	aws cloudformation create-stack \
		--profile $(PROFILE) \
		--stack-name $(STACK_NAME) \
		--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
		--template-body file://lambda.yml \
		--tags Key=Name,Value=$(FUNCTION_NAME) && sleep 61; \
	aws lambda update-function-code \
		--profile $(PROFILE) \
		--function-name $(FUNCTION_NAME) \
		--zip-file fileb://function.zip;

.PHONY: update
update: zip
	unset AWS_DEFAULT_REGION; \
	aws configure --profile $(PROFILE); \
	aws cloudformation update-stack \
		--profile $(PROFILE) \
		--stack-name $(STACK_NAME) \
		--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM\
		--template-body file://lambda.yml \
		--tags Key=Name,Value=$(FUNCTION_NAME); \
	aws lambda update-function-code \
		--profile $(PROFILE) \
		--function-name $(FUNCTION_NAME) \
		--zip-file fileb://function.zip;
