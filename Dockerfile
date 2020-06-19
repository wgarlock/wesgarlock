# Future addition
FROM python:3.6-alpine3.12

ADD /requirements.txt app/requirements.txt
ADD /wheels app/wheels
ADD /project app/project
ADD /manage.py app/manage.py
ADD /tenant_context_manage.py app/tenant_context_manage.py

RUN set -ex \
    && apk add --no-cache --virtual .build-deps git libffi-dev libxml2-dev libxslt-dev postgresql-dev jpeg-dev build-base memcached \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r app/requirements.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps \
    && cd app && ls -all

ADD .env /app
WORKDIR /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "project.wsgi:application"]