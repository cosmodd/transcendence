FROM python:3.9-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the entrypoint.sh file into the working directory
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

RUN apk update && apk add openssl
RUN openssl req -x509 -newkey rsa:4096 -keyout /key.pem -out /cert.pem -sha256 -days 3650 -nodes \
	-subj "/C=FR/ST=Nice/L=Nice/O=42 Nice/OU=pforesti/CN=pforesti"

# Run the django app on port 8000 on every interface
ENTRYPOINT ["./entrypoint.sh"]
