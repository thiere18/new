FROM python:3.8
# LABEL org.opencontainers.image.source https://github.com/sigularusrex/cura

RUN mkdir /app
WORKDIR /app

# RUN apt update -y \
#     && apt install nginx curl vim -y \
#     && apt-get install software-properties-common -y \
#     && add-apt-repository -r ppa:certbot/certbot -y \
#     && apt-get update -y \
#     && apt-get install python3-certbot-nginx -y \
#     && apt-get clean

RUN apt update && \
    apt install -y postgresql-client

COPY pyproject.toml ./

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .
# EXPOSE 80

# STOPSIGNAL SIGTERM

CMD ["python", "-m", "main"]
