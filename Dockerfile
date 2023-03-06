FROM python:alpine
WORKDIR /app
COPY . .
RUN python3 -m pip install -r requirements.txt
RUN echo "* * * * * source /app/.env; python3 /app/main.py" >> /var/spool/cron/crontabs/root
CMD ["crond", "-f"]
