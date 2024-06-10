FROM python:3.12-slim

EXPOSE 8080

ARG build_version="none"
ENV BUILD_VERSION ${build_version}

WORKDIR /app

COPY src src/
COPY static static/
COPY templates templates/
COPY pyproject.toml main.py server.sh README.md ./
RUN echo ${BUILD_VERSION} > templates/version.txt

RUN mkdir static/converted &2>/dev/null
RUN pip install .

RUN chmod +x /app/server.sh
RUN chown 1000:1000 /app/
RUN chown 1000:1000 static/converted

USER 1000

CMD ["/app/server.sh"]