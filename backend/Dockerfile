FROM quay.io/fedora/python-312:latest

# USER 1001

WORKDIR /app

COPY ./ ./

RUN pip3 install --upgrade pip
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install --no-cache-dir -r requirements.txt

RUN export WEB_CONCURRENCY=$(nproc)

EXPOSE 8000

CMD ["./entrypoint.sh"]
