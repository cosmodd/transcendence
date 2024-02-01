FROM python:3.9-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt


# Run the django app on port 8000 on every interface
ENTRYPOINT [ "./entrypoint.sh" ]
