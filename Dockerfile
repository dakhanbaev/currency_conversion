FROM python:3.9-slim


COPY . .

WORKDIR .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN chmod +x entrypoint.sh

EXPOSE 8000
