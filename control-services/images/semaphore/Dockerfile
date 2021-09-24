# https://github.com/playniuniu/docker-ansible-semaphore/blob/master/Dockerfile
FROM alpine:latest

ENV PACKAGE="curl git ansible mysql-client openssh-client openssh sshpass rsync" \
    SEMAPHORE_DOWNLOAD_URL="https://github.com/ansible-semaphore/semaphore/releases/download/v2.1.0/semaphore_linux_amd64" \
    SEMAPHORE_PLAYBOOK_PATH="/data" \
    GIN_MODE="release"

COPY entrypoint.sh /usr/bin/entrypoint.sh
COPY ansible.cfg /etc/ansible/ansible.cfg

RUN apk add --update --no-cache ${PACKAGE} \
    && curl -sSL ${SEMAPHORE_DOWNLOAD_URL} -o /usr/bin/semaphore \
    && chmod +x /usr/bin/semaphore \
    && rm -rf /var/cache/apk/*

RUN mkdir /data
COPY ./semaphore_config.sh /data

EXPOSE 3000

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
CMD ["/usr/bin/semaphore", "-config", "/data/semaphore_config.json"]
