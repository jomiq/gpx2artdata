FROM python:3.12-slim

EXPOSE 8080
WORKDIR /app

COPY src src/
COPY static static/
COPY templates templates/
COPY pyproject.toml main.py server.sh README.md ./

RUN mkdir static/converted &2>/dev/null
RUN pip install .

RUN chmod +x /app/server.sh
RUN chown 1000:1000 /app/
RUN chown 1000:1000 static/converted

USER 1000

CMD ["/app/server.sh"]