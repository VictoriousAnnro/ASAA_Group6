### Project Guide
This file will explain how to run the project.
URL for the repository:
https://github.com/VictoriousAnnro/ASAA_Group6/tree/AMReport

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
To create an admin account, the website must first be running using Docker Compose. From the command prompt , docker-compose run --rm website sh -c "python manage.py createsuperuser"  command need to run after that it opens an interactive prompt where need to provide a username, email address, and password. After providing the information it will confirm that  a superuser account is created in the system database. The admin has accessed to interface of the website.  Admin can see the user information.
After the admin account is created, the admin can log in to the admin panel using their username and password. To add a new car, the admin navigates to the product section and fills in the required information, such as the car name, model, engine type, available color , and price. Once the information is saved, the car and its variants are stored in the database and immediately become visible on the website. The admin can update or delete existing cars and variants. Any changes made by the admin are reflected in real time on the website, ensuring that product information remains consistent and up to date. 
Admin can see the cart, cart items, order and order item. Admin can remove the order after it is done and also remove the items from the cart if they are no longer available.
 
## Access Website
The website is hosted at: http://127.0.0.1:8000/
The user needs to be registered in order to add items in the cart or order the car. After logging in as a user , they can select the car and customize as they desire and can add the quantity of the product and then add it to the cart. After that they can place the order and the order will be stored in the database. If an unauthenticated user attempts to add a car to the cart or access the cart page, the system automatically redirects the user to the login page to ensure that all purchasing actions are associated with a valid customer account.

