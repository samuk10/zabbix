FROM zabbix/zabbix-server-pgsql:ubuntu-6.4-latest

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
      whois \
      python3-bs4 \
      python3-requests \
      python3-cloudscraper && \
    rm -rf /var/lib/apt/lists/*

USER zabbix