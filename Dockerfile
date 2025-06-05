FROM python:3.10-slim
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .


RUN pip install --upgrade pip \ 
    && pip install -r requirements.txt

EXPOSE 5000
ENV RUNNING_IN_DOCKER=true

CMD ["python", "run.py"]
