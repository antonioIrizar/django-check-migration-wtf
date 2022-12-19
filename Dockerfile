FROM python:3.9-slim

ENV HOMEDIR=/app/ \
  TERM=vt100 \
  C_FORCE_ROOT=1 \
  PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN buildDeps="g++ gcc git libc6-dev" \
  && apt-get update && apt-get install --assume-yes --no-install-recommends \
    $buildDeps \
    gdal-bin \
    gettext \
    libcairo2 \
    libpango1.0-0 \
    libpango1.0-dev \
    make \
    postgresql-client \
    libsasl2-dev \
    libsasl2-modules \
    libssl-dev \
  && python -m pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false $buildDeps \
  && apt-get clean

WORKDIR $HOMEDIR

COPY . $HOMEDIR

CMD tail -f /dev/null