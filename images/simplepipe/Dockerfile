FROM ubuntu:21.10
# Install necessary packages.
# Including rm -rf /var/lib/apt/lists/* saves memory by removing
# cached items related to the upgrade command
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get -y upgrade && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/* 

WORKDIR /simplepipe
COPY simplepipe .
RUN pip install -e .
# Run as non-root user:
RUN useradd --create-home appuser
USER appuser
ENTRYPOINT ["python3", "app.py"]