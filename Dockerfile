FROM python:3.8-slim

RUN apt update && apt install -y curl postgresql libpq-dev build-essential unzip

RUN curl -sL https://deb.nodesource.com/setup_13.x | bash -
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt update && apt install -y nodejs yarn

# Chrome driver install
RUN curl -O https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
  apt install -y ./google-chrome-stable_current_amd64.deb && rm google-chrome-stable_current_amd64.deb
RUN curl -O https://chromedriver.storage.googleapis.com/81.0.4044.69/chromedriver_linux64.zip && \
  unzip chromedriver_linux64.zip && chmod +x chromedriver && mv chromedriver /usr/bin/chromedriver && \
  rm chromedriver_linux64.zip



COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 80

RUN cd web && yarn && yarn prod && cd ..

CMD ["gunicorn", "--bind=0.0.0.0:80", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "debug", "app:application"]
