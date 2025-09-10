FROM python:3.10.2-slim
ADD . /pulsar_bot
WORKDIR /pulsar_bot
RUN pip3.10 install --upgrade pip
RUN pip3.10 install pipenv
RUN pipenv install --system --ignore-pipfile
CMD [ "python3.10", "bot.py" ]
