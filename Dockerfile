FROM python:3.10

ARG APP_USER=django
ARG SERVICE_NAME=app

# Create a user and group for the application
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER} -b /${SERVICE_NAME}
ENV PROJECT_ROOT=/${SERVICE_NAME}

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r /app/requirements.txt

# Install runtime dependencies (using apt-get for Debian-based image)
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

RUN  pip install django
# RUN pip install django-environ==0.11.2

# Install the required Python packages directly
RUN pip install djangorestframework==3.15.2 \
    djangorestframework-simplejwt==5.3.1 \
    djangorestframework-camel-case==1.4.2 \
    django-filter==24.3 \
    django-environ==0.11.2 \
    numpy==2.1.3 \
    pillow==11.0.0 \
    pre_commit==4.0.1 \
    psycopg2-binary==2.9.10 \
    python-dateutil==2.9.0.post0 \
    drf-yasg==1.21.8 \
    whitenoise \
    sentry-sdk[django]

RUN pip install daphne

# Copy the application source code into the container
COPY ./ /${SERVICE_NAME}/

COPY init.sh /${SERVICE_NAME}/init.sh
RUN chmod +x /${SERVICE_NAME}/init.sh

# Set permissions for the application files
RUN chown -R ${APP_USER}:${APP_USER} /${SERVICE_NAME}/ && chmod +x /${SERVICE_NAME}/*.sh

# Set the working directory and user
WORKDIR /${SERVICE_NAME}/
USER ${APP_USER}

# Set the Python path
ENV PYTHONPATH "${PYTHONPATH}:${PROJECT_ROOT}"

# Set the entrypoint and default command
ENTRYPOINT ["/bin/bash","/app/init.sh"]
CMD ["app"]
