FROM debian:12-slim AS builder

WORKDIR /srv/scipo

RUN apt-get update \
    && apt-get -y install --no-install-recommends \
    git \
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

RUN git clone https://github.com/CERIT-SC/scipion-helm-charts.git /opt/scipion-helm-charts

## Base stage
FROM debian:12-slim AS base

WORKDIR /srv/scipo

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3 \
    curl \
    ca-certificates \
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

# Create user web
RUN useradd -u 1000 -m web -s /bin/bash \
    && chown -R web /srv/scipo

# TODO Install kubectl for testing purpose (kubectl python api does not need it probably)
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x kubectl

# Install Helm. This is required for deploying the instances
RUN cd /tmp \
    && curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 \
    && chmod 700 get_helm.sh \
    && ./get_helm.sh \
    && rm ./get_helm.sh

# Copy scipion-docker helm chart for deploying the Scipion app
COPY --from=builder /opt/scipion-helm-charts/scipion-docker/v2.0 /opt/scipion-docker-chart
RUN chown -R web:web /opt/scipion-docker-chart

# Copy folder with the app sources
COPY ./scipo /srv/scipo

USER web

CMD [ "/bin/bash", "/srv/scipo/init.sh" ]
