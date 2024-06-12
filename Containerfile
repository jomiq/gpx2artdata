FROM python:3.12-slim

EXPOSE 8080

ARG git_hash="local build"
ARG website_url=""

ENV GIT_HASH ${git_hash}
ENV WEBSITE_URL ${website_url}

WORKDIR /app

COPY src src/
COPY static static/
COPY templates templates/
COPY pyproject.toml main.py server.sh README.md ./
RUN echo ${GIT_HASH} > templates/githash.txt
RUN if [ "${WEBSITE_URL}" != "" ]; then echo "${WEBSITE_URL}/static" > templates/static_url.txt ; fi;

RUN pip install .[server]

RUN chmod +x /app/server.sh
RUN chown 1000:1000 /app/

USER 1000

CMD ["/app/server.sh"]