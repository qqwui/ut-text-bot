FROM python:3

WORKDIR	/usr/src/app

# ADD https://github.com/qqwui/ut-text-bot.git .
ADD main.py requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]
