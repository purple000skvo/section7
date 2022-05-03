FROM python:3.6.9-alpine

COPY . /code
WORKDIR /code

RUN apk --update --upgrade add --no-cache  gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

RUN python -m pip install pip==20.2.4
#COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
#COPY . .
CMD [ "python", "app.py" ]