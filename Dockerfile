# Use of a custom base image for AWS Lambda:
# https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-create-alt
# https://github.com/aws/aws-lambda-python-runtime-interface-client/
FROM python:3.11.3

# Add non-root system user
RUN addgroup --system docker &&\
    useradd --gid docker --system docker

ARG aws_default_region
ARG aws_access_key_id
ARG aws_secret_access_key

# Use AWS access key instead of a role to allow execution of the image in a local environment.
# If the image would only run inside an AWS service (e.g. Lambda function), we could use a service role.
ENV AWS_DEFAULT_REGION=$aws_default_region \
    AWS_ACCESS_KEY_ID=$aws_access_key_id \
    AWS_SECRET_ACCESS_KEY=$aws_secret_access_key \
    BROWSE_AI_ROBOT_ID="/il-apr-comparator/browse-ai/robot-id" \
    BROWSE_AI_API_KEY="/il-apr-comparator/browse-ai/api-key" \
    SNS_TOPIC="/il-apr-comparator/sns/topic"

# Create working directory for image and cd into it
WORKDIR /app

COPY ./app .

RUN chown --recursive docker:docker /app

RUN pip install --no-cache-dir -r requirements.txt

# Ignore info about deletion of apt-get lists.
# The lists are necessary for the installation of Chrome and will be removed afterwards (see below).
# hadolint ignore = DL3009
RUN apt-get update &&\
    apt-get upgrade --assume-yes

# Install aws-lambda-cpp build dependencies (this code is taken directly from the AWS documentation)
# Ignore:
#   - warning about unspecified package versions
#   - info about potential installation of additional packages
# hadolint ignore = DL3008, DL3015
RUN apt-get install --assume-yes \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

# Install the runtime interface client (this code is taken directly from the AWS documentation)
# Ignore warning about unspecified package versions
# hadolint ignore = DL3013
RUN pip install --no-cache-dir --target /app awslambdaric

# Install latest stable version of Google Chrome
RUN curl --location --remote-name  "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" &&\
    apt-get install --assume-yes --no-install-recommends ./google-chrome-stable_current_amd64.deb &&\
    rm ./google-chrome-stable_current_amd64.deb

# Remove apt-get package lists to save space
RUN rm --recursive /var/lib/apt/lists/*

# Install latest stable version of ChromeDriver
# https://chromedriver.chromium.org/getting-started
# https://chromedriver.chromium.org/downloads/version-selection
RUN latest_release=$(curl -L "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") &&\
    curl --location "https://chromedriver.storage.googleapis.com/$latest_release/chromedriver_linux64.zip" > chromedriver.zip &&\
    unzip chromedriver.zip -d /usr/local/bin &&\
    rm chromedriver.zip

# Run container as non-root system user
USER docker

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD ["main.lambda_handler"]
