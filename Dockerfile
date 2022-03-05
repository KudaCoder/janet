# syntax=docker/dockerfile:1

FROM python:3.8

EXPOSE 80

RUN mkdir -p /app
WORKDIR /app

RUN apt-get update
RUN apt install -y portaudio19-dev python3-pyaudio
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install python-dotenv

COPY . .

CMD [ "python3", "janet.py"]