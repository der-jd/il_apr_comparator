FROM python:3.11.3

# Add non-root system user
RUN groupadd --system docker &&\
    useradd --gid docker --system docker

# Create working directory for image and cd into it
WORKDIR /app

RUN chown --recursive docker:docker /app

COPY ./app .

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt

# Upgrade packages and remove package lists afterwards to save space
RUN apt-get update &&\
    apt-get upgrade --assume-yes &&\
    rm /var/lib/apt/lists/*

# Install latest stable version of Google Chrome
RUN curl --location --remote-name  "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" &&\
    apt-get install --no-install-recommends ./google-chrome-stable_current_amd64.deb --assume-yes &&\
    rm ./google-chrome-stable_current_amd64.deb

# Install latest stable version of ChromeDriver
# https://chromedriver.chromium.org/getting-started
# https://chromedriver.chromium.org/downloads/version-selection
RUN latest_release=$(curl -L "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") &&\
    curl --location "https://chromedriver.storage.googleapis.com/$latest_release/chromedriver_linux64.zip" > chromedriver.zip &&\
    unzip chromedriver.zip -d /usr/local/bin &&\
    rm chromedriver.zip

# Run container as non-root system user
USER docker

CMD ["python3", "main.py"]
