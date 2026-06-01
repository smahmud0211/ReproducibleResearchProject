FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    make \
    wget \
    gdebi-core \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.9.38/quarto-1.9.38-linux-arm64.deb \
    && gdebi --non-interactive quarto-1.9.38-linux-arm64.deb \
    && rm quarto-1.9.38-linux-arm64.deb

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["make", "all"]