FROM python:3

RUN apt-get update && apt-get -y install curl
             
            
# set timezone to Europ/Berlin
RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime
RUN apt-get install -y tzdata
RUN dpkg-reconfigure -f noninteractive tzdata

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn aiofiles
RUN pip install fastapi_websocket_pubsub








