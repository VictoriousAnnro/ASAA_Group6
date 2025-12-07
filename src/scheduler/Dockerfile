# Use an official Python runtime as an image
FROM python:latest

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction 
# creates a directory with this name if it doesn’t exist
WORKDIR /scheduler

COPY . .

# Install any needed packages specified in requirements.txt
#COPY ./requirements.txt /scheduler/requirements.txt
#COPY . /scheduler

RUN pip install -r requirements.txt

# The EXPOSE instruction indicates the ports on which a container 
# will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000

# Run scheduler.py when the container launches
# doesnt work for some reason
CMD [ "python", "./scheduler.py" ]
#CMD python scheduler.py