FROM python:3.8-alpine

RUN pip install pipenv

RUN mkdir -p /smfp

COPY . /smfp

RUN cd /smfp \
    && pipenv --python /usr/local/bin/python install --system

CMD ["/usr/local/bin/python", "/smfp/main.py"]