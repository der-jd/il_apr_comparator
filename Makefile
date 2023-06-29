lint: lint-cfn hadolint lint-python typecheck-python

lint-cfn:
	for file in $$(find ./cloudformation -name "*.yaml"); do \
		echo "lint $$file..."; \
		cfn-lint "$$file" || exit; # Use 'exit' here to return immediately after an error. Otherwise the for loop may ignore the error. \
	done

hadolint:
	hadolint Dockerfile

lint-python:
	for file in $$(find . -name "*.py"); do \
		echo "lint $$file..."; \
		pylint "$$file" || exit; # Use 'exit' here to return immediately after an error. Otherwise the for loop may ignore the error. \
	done

typecheck-python:
	pyright


build-and-run: build run-lambda-image run-lambda-function

build:
	docker build \
		--build-arg aws_default_region=$(AWS_REGION) \
		--build-arg aws_access_key_id=$(AWS_ACCESS_KEY) \
		--build-arg aws_secret_access_key=$(AWS_SECRET_KEY) \
		--tag il-apr-comparator .


# Local test of Lambda function: https://github.com/aws/aws-lambda-python-runtime-interface-client/
setup-local-lambda-test:
	mkdir -p ~/.aws-lambda-rie && \
    curl -Lo ~/.aws-lambda-rie/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie && \
    chmod +x ~/.aws-lambda-rie/aws-lambda-rie

run-lambda-image:
	docker run -d -v ~/.aws-lambda-rie:/aws-lambda -p 9000:8080 \
    	--entrypoint /aws-lambda/aws-lambda-rie \
    	il-apr-comparator:latest \
        /usr/local/bin/python -m awslambdaric main.lambda_handler

run-lambda-function:
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
