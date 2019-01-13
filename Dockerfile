# Use phusion/baseimage as base image. To make your builds
# reproducible, make sure you lock down to a specific version, not
# to `latest`! See
# https://github.com/phusion/baseimage-docker/blob/master/Changelog.md
# for a list of version numbers.
FROM phusion/baseimage:0.11

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# ...put your own build instructions here...
RUN apt-get update && apt-get install -y \ 
    python3 \
    python3-dev \ 
    python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN ["chmod", "+x", "start.sh"]
RUN ["sh", "start.sh"]
# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*