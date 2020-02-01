FROM debian:buster

RUN DEBIAN_FRONTEND=noninteractive\
    apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install \
        wget \
        xvfb \
        unzip \
        python3 \
        python3-pip \
        wget \
        chromium \
        chromium-driver && \
    apt-get clean autoclean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY xml2pdf.py xml2pdf.py

ENV WORK_DIR /work
RUN mkdir -p $WORK_DIR

ENTRYPOINT ["/bin/bash","-c","find $WORK_DIR -name '*.json.xml' -exec python3 xml2pdf.py {} \\;"]