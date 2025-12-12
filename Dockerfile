# Use official Python slim image
FROM python:3.11-slim

WORKDIR /app

# install system deps needed for some Python packages (psycopg2 etc)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev curl netcat && \
    rm -rf /var/lib/apt/lists/*

# copy dependency list first (cache)
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# copy project code
COPY . /app/

# ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

# start the app
CMD ["/app/entrypoint.sh"]
