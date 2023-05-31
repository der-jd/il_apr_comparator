lint: lint-cfn hadolint lint-python

lint-cfn:
	for file in $$(find ./aws -name "*.yaml"); do \
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
