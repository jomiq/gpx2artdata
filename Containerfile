FROM python:3.12-alpine3.20

EXPOSE 8000
WORKDIR /app

COPY src src/
COPY static static/
COPY templates templates/
COPY pyproject.toml main.py server.sh README.md ./

RUN pip install .

RUN chmod +x server.sh
RUN chown 1000:1000 /app

USER 1000

CMD ["/app/server.sh"]