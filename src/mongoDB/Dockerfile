FROM mongo:latest

WORKDIR /DockerMongoDB

# TODO
# NEED TO ADD VOLUME. Better to do with Docker Compose:
# https://docs.docker.com/engine/storage/volumes/#use-a-volume-with-docker-compose
# How to access DB from outside?

#Copy everything from this folder (mongoDB) into /DockerMongoDB
COPY . ./

#Use this if we need to install something specific
#RUN ....

# mongo:1 is tag for image
# docker build -t mongo:1 src/mongoDB/Dockerfile

# Create and run a new container from the image (port 27017)
# docker run -d -p 27017:27017 --name=mongoDB --rm mongo:1
# -d runs in detached mode, meaning the terminal you run the command in will not be 'overtaken' by the container (cluttered with log info and unable to perform commands)

# Connect to MongoDB instance using the MongoDB shell:
# docker exec -it mongoDB mongosh