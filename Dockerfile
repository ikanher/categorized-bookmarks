FROM python:3.7-alpine

COPY ./categorized-bookmarks /app

WORKDIR /app

RUN apk add --no-cache libpq postgresql-dev py-sqlalchemy && \
    apk add --no-cache --virtual .build-deps build-base python3-dev libffi-dev && \
    pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps && \
    adduser -S app && \
    chown -R app /app

USER app

CMD ["gunicorn", "--preload", "--bind", "0.0.0.0:5000", "--workers", "1", "application:app"]
