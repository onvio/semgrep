FROM returntocorp/semgrep:latest

USER root

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY . /opt/semgrep/

RUN mkdir /var/reports \
    && chmod +x /opt/semgrep/start.sh

ENTRYPOINT ["/opt/semgrep/start.sh"]