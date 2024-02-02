FROM zabbix/zabbix-server-pgsql:ubuntu-6.4-latest

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt install -y \
  whois \
  python3-pip && \
  pip install bs4 cloudscraper requests && \
  rm -rf /var/lib/apt/lists/*

USER zabbix
