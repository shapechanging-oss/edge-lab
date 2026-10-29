FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      systemd systemd-sysv dbus sudo vim less curl ca-certificates \
      iproute2 iputils-ping dnsutils tcpdump nftables openssl netcat-openbsd \
      procps sysstat strace lsof psmisc htop iotop \
      nginx python3 python3-venv git jq shellcheck apache2-utils \
      postgresql-client mysql-client prometheus-node-exporter \
 && rm -rf /var/lib/apt/lists/* \
 && useradd -m -s /bin/bash -G sudo dev \
 && echo 'dev ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/dev
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
