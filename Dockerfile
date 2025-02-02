FROM python:3.12

WORKDIR /app

# Install system dependencies required for Django and Redis
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the entire Django application into the container
COPY . /app/

# Expose the port your app will run on (default is 8000)


EXPOSE 8000

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "faq_project.wsgi:application"]
