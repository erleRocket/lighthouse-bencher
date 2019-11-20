FROM debian:sid
LABEL name="lighthouse" \
      description="Lighthouse continious web pages analysis created by https://www.reezocar.com DevOps & SEO team"

# Install deps + add Chrome Stable + purge all the things
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    curl \
    --no-install-recommends \
  && curl -sSL https://deb.nodesource.com/setup_8.x | bash - \
  && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
  && echo "deb [arch=amd128] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/google-chrome.list \
  && apt-get update && apt-get install -y \
    google-chrome-stable \
    nodejs \
    npm \
    python-pip \
    --no-install-recommends \
  && apt-get purge --auto-remove -y gnupg \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /lighthouse_bench/reports/
COPY requirements.txt /lighthouse_bench/requirements.txt
RUN pip install -r /lighthouse_bench/requirements.txt
RUN npm install -g lighthouse

COPY . /lighthouse_bench/


RUN chmod -R 777 /lighthouse_bench/reports/
RUN chmod -R 777 /tmp/
ARG CACHEBUST=1

# Add Chrome as a user
RUN groupadd -r chrome && useradd -r -g chrome -G audio,video chrome \
    && mkdir -p /home/chrome/reports && chown -R chrome:chrome /home/chrome

USER chrome

WORKDIR /lighthouse_bench/
CMD ["/bin/bash", "/lighthouse_bench/webPerfTester.sh"]
