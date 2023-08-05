FROM python:latest

COPY . .
ENV TYPE=huggingface
RUN ./scripts/install.sh

CMD ["sh", "-c", "./scripts/start.sh"]
