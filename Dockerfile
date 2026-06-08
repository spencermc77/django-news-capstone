# Use Python 3.11 as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first so Docker can cache dependency installation
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full Django project into the container
COPY . .

# Expose port 8000 for the Django development server
EXPOSE 8000

# Run the Django development server inside the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]