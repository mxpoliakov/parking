FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \ 
    python3 \
    python3-dev \ 
    python3-pip \
    libglib2.0-0

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN ["chmod", "+x", "start.sh"]
CMD ["sh", "start.sh"]