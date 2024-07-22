FROM python:3.11-slim AS builder
# Set the working directory in the container to /app
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . .
# Install build dependencies for cryptography
RUN pip install --target=/app requests pygithub

# Use a minimal distroless image for production
FROM gcr.io/distroless/python3-debian12

# Copy the entire application and its dependencies from the builder stage
COPY --from=builder /app /app

# Set the working directory in the container to /app
WORKDIR /app

# Set the PYTHONPATH to /app to ensure the Python interpreter can find our application
ENV PYTHONPATH /app

# Define the command to run the application
ENTRYPOINT ["python3", "/app/main.py"]

