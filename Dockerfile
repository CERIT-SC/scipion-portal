FROM debian:12-slim AS builder

WORKDIR /srv/scipo

RUN apt-get update \
    && apt-get -y install --no-install-recommends \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-pkgconfig \
    default-libmysqlclient-dev \
    build-essential \
    # install nodejs
    curl \
    ca-certificates \
    gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    # set up version
    && NODE_MAJOR=18 \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install nodejs -y

COPY ./requirements.txt /srv/scipo
COPY ./package.json /srv/scipo

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -r requirements.txt \
    && npm install

## Base stage
FROM debian:12-slim AS base

WORKDIR /srv/scipo

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3 \
    default-libmysqlclient-dev \
    nano \
    less \
    # Set the correct timezone
    && ln -fs /usr/share/zoneinfo/Europe/Prague /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    # clean after installation
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

# Get python and JS packages
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /srv/scipo/node_modules /srv/scipo/node_modules

ENV PATH="/opt/venv/bin:$PATH"

# create user web
RUN useradd -u 1000 -m web -s /bin/bash \
    && chown -R web /srv/scipo

# install kubectl for testing purpose (kubectl python api does not need it probably)
#RUN apt update && apt install -y ca-certificates curl gpg
#RUN curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /etc/apt/keyrings/kubernetes-archive-keyring.gpg
#RUN echo "deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list
#RUN apt update && apt install -y kubectl
RUN apt update && apt install -y curl \
    && curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && echo "root:a" | chpasswd

USER web

# Copy folder with the app sources
ADD ./scipo /srv/scipo

CMD [ "/bin/bash", "/srv/scipo/init.sh" ]
