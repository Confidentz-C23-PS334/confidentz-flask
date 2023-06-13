# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /confidentz-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ["app.py", "confidentz_model.h5", "."]
MKDIR uploads

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
