FROM python:3.12-slim

EXPOSE 8080

ARG production="True"
ARG build_version="unknown"
ARG website_hostname=""
ARG static_url=""

ENV PRODUCTION ${production}
ENV BUILD_VERSION ${build_version}
ENV WEBSITE_HOSTNAME ${website_hostname}
ENV STATIC_URL ${static_url}

WORKDIR /app

COPY src src/
COPY static static/
COPY templates templates/
COPY pyproject.toml main.py server.sh README.md ./

RUN pip install .[server]

RUN chmod +x /app/server.sh
RUN chown 1000:1000 /app/

USER 1000

CMD ["/app/server.sh"]