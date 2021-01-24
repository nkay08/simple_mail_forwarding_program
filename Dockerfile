FROM alpine:3.13

RUN apk update \
    && apk add python3 py3-pip \
    && ln -s /usr/bin/python3 /usr/bin/python

RUN pip install pipenv

RUN mkdir -p /smfp

COPY . /smfp

RUN cd /smfp \
    && pipenv --python /usr/bin/python3 install --system

CMD ["/usr/bin/python3", "/smfp/main.py"]