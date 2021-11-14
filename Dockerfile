ARG ARCH=
FROM ${ARCH}/alpine:3.12
#FROM ${ARCH}/debian:buster-slim

RUN apk add --no-cache python3 py3-pip 
RUN apk add --no-cache gcc \
                       libc-dev \
                       python3-dev

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn aiofiles
RUN pip install fastapi_websocket_pubsub
RUN pip install fastapi_utils

WORKDIR /root
COPY server.py server.py
COPY assets assets
COPY data data
COPY bomberman bomberman

CMD ["uvicorn","server:app","--host","0.0.0.0", "--port","8066"]








