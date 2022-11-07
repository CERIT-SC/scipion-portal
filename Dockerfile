FROM debian:11-slim AS builder

WORKDIR /srv/scipo

RUN apt-get update \
    && apt-get -y install python3-pip

COPY ./requirements.txt /srv/scipo

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /srv/scipo/wheels -r requirements.txt

## Base stage
FROM debian:11-slim AS base

WORKDIR /srv/scipo

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3 \
    python3-dev \
    python3-pip \
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
COPY --from=builder /srv/scipo/wheels /wheels
COPY --from=builder /srv/scipo/requirements.txt .

RUN pip install --no-cache /wheels/* \
    # create user web
    && useradd -u 1000 -m web -s /bin/bash \
    && chown -R web /srv/scipo

## Final stage
FROM base

USER web

# Copy folder with the app sources
ADD ./scipo /srv/scipo

# Prepare application
RUN echo "alias pyma='python3 manage.py'" >> ~/.bashrc \
    && echo "alias ll='ls $LS_OPTIONS -l'" >> ~/.bashrc \
    && echo "alias tailf='tail -f'" >> ~/.bashrc

CMD [ "/bin/bash", "/srv/scipo/init.sh" ]
