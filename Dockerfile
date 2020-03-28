FROM python:3.7

# /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd
RUN set -x && \
  apt-get update && \
  apt-get install -y --no-install-recommends vim mecab libmecab-dev mecab-ipadic-utf8 sudo && \
  apt-get clean -y && \
  git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /usr/local/src/mecab-ipadic-neologd && \
  /usr/local/src/mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y -a && \
  pip install --upgrade pip && \
  pip install pipenv
