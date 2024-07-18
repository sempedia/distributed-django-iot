# Set the Python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# create a virtual env 
RUN python -m venv /opt/env

# Set the virtual env as the current location
ENV PATH=/opt/env/bin:$PATH

# Upgrade PIP
RUN pip install --upgrade pip 

# Set python related env variables:
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Install os dependencies for our mini VM 
RUN apt-get update && apt-get install -y \
    # for postgres
    libpq-dev \
    # for Pillow
    libjpeg-dev \
    # for CairoSVG
    libcairo2 \
    # other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the mini VM's 'code' directory 
RUN mkdir -p /code

# Set the working directory to that same 'code' folder we created \
WORKDIR /code

# Copy the requirements.txt file into the container 
COPY requirements.txt /tmp/requirements.txt

# Copy the django project code from /src local into the container's working dir /code:
COPY ./src /code


# Install the python project requirements into the container's working dir
RUN pip install -r /tmp/requirements.txt

# database isn't available during build
# run any other commnads that do not need the database
# such as:
# RUN python manage.py collectstatic --noinput

# set the Django default project name into the container
ARG PROJ_NAME="core"

# create a bash script to run the Django project
# this script will execute at runtime when 
# this container starts and the database is availeble
RUN printf "#!/bin/bash\n" > ./paracord_runner.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./paracord_runner.sh && \
    printf "python manage.py migrate --no-input\n" >> ./paracord_runner.sh && \
    printf "gunicorn ${PROJ_NAME}.wsgi:application --bind \"0.0.0.0:\$RUN_PORT\"\n" >> ./paracord_runner.sh

# make the bash script executable
RUN chmod +x paracord_runner.sh

# Clean up apt cache to reduce image size 
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Run the Django project via the executable runtime script when the container starts
CMD ./paracord_runner.sh