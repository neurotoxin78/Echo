FROM mcr.microsoft.com/playwright:v1.28.1-jammy AS base
FROM base
RUN apt-get update -y && apt-get install -y python3-pip
WORKDIR /app
USER pwuser
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]
