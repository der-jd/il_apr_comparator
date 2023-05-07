FROM python:3.11.3

# Add non-root system user
RUN useradd --system docker

# Create working directory for image and cd into it
WORKDIR /app

COPY ./app .

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt

RUN apt-get update &&\
    apt-get upgrade --assume-yes

# Install latest stable version of Google Chrome
RUN curl --location --remote-name  https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&\
    apt-get install ./google-chrome-stable_current_amd64.deb --assume-yes

# Install latest stable version of ChromeDriver
# https://chromedriver.chromium.org/getting-started
# https://chromedriver.chromium.org/downloads/version-selection
RUN latest_release=$(curl -L https://chromedriver.storage.googleapis.com/LATEST_RELEASE) &&\
    curl --location https://chromedriver.storage.googleapis.com/$latest_release/chromedriver_linux64.zip > chromedriver.zip &&\
    unzip chromedriver.zip -d /usr/local/bin

# Run container as non-root system user
USER docker

#CMD ["python3", "main.py"]
