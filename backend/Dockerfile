FROM quay.io/fedora/python-312-minimal:latest

USER 1001

WORKDIR /app

COPY --chown=1001:1001 ./ ./

RUN pip3 install --upgrade pip
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["./entrypoint.sh"]
