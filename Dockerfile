FROM python:3.11.3

# Add non-root system user
RUN groupadd --system docker &&\
    useradd --gid docker --system docker

# Create working directory for image and cd into it
WORKDIR /app

COPY ./app .

RUN chown --recursive docker:docker /app

# Ignore info concerning multiple consecutive 'RUN' instructions
# hadolint ignore = DL3059
RUN pip install --no-cache-dir -r requirements.txt

# Ignore info concerning deletion of apt-get lists.
# The lists are necessary for the installation of Chrome and will be removed afterwards (see below).
# hadolint ignore = DL3009
RUN apt-get update &&\
    apt-get upgrade --assume-yes

# Install latest stable version of Google Chrome
RUN curl --location --remote-name  "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" &&\
    apt-get install --no-install-recommends ./google-chrome-stable_current_amd64.deb --assume-yes &&\
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

CMD ["python3", "/app/main.py"]
