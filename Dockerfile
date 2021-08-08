FROM python:3
ENV PYTHONUNBUFFERED=1
COPY .aws /root/.aws
ADD . //camera-node
WORKDIR /camera-node
RUN pip install -r requirements.txt