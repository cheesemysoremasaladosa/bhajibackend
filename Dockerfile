FROM python:3.12-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt


RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY ./app /code/app
COPY ./static /code/static
COPY ./.config.docker /code/.config
EXPOSE 8000
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]