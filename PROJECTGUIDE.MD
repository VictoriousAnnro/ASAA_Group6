### Project Guide
This file will explain how to run the project.

## Dependencies
The user should have these things installed on their computer:
- Docker
Docker Desktop is recommended.

## How to run
Make sure the Docker Daemon is running. Navigate to the /src folder, and run this command:
docker compose up
This will pull the images and create the containers. 

Due to problems with the website container, it will have to be manually re-started, and the scheduler.py must be run manually. Using Docker Desktop, once all other containers have started, navigate to the 'scheduler' container and re-start it. Access the shell of the container, and run this command:
python scheduler.py
Now all systems are available and running.

## Add cars to website
**Explain how to make admin user, and how to add car + car variants to website**

## Access Website
The website is hosted at: http://127.0.0.1:8000/
**Explain how to login, how to add car to cart, and how to access cart**