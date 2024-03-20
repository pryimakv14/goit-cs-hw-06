FROM python:3.9

WORKDIR /var/www/app

COPY requirements.txt /var/www/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["python", "-u", "main.py"]