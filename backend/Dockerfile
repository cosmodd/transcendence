FROM python:3.9

# Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the entrypoint.sh file into the working directory
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Run the django app on port 8000 on every interface
ENTRYPOINT ["./entrypoint.sh"]
