# Source Code

# TODO - automate experiment
We can probably do this by creating a button on the website, that calls the relevant URLs with hardcoded values when clicked.

Lets assume I've created a car for the website, and that I'm now logged in as a non-admin user.
I did something similar in src\website\app\templates\header.html
Near the car-image I added this button <a id="add-to-cart-btn" class="input-group-text" href="#"><i class="fas fa-plus"></i></a>
I added a script at the bottom of the file, where I added an eventlistener to that button. When clicked, it makes a GET-request to the '/order/add-to-cart' URL with hardcoded values. While nothing shows up on the screen, if you navigate to http://127.0.0.1:8000/order/cart you'll see that a car has been added to cart.

After we've added something to the cart, we just need to do the checkout by making a POST-call to the 'checkout/<str:cart_id>/' URL. We need to give it the cart_id, and the customer details.
I think all values except the cart_id can be hardcoded. When we add something to the cart, we need to get the cart_id somehow, so we can pass it to the checkout.

So:
- We can just add more functionality to the button I made
- Figure out how to get the cart_id when car has been added to cart. We don't know if the cart_id is always the same, so we can't hardcode it.
- Expand the functionality of the button to make a POST-request to the 'checkout/<str:cart_id>/' URL with hardcoded values about the customer. They DON'T need to be randomized every time.
- Then we just click the button a bunch of times and check the outputs in the scheduler-log

# To create an admin user
The image/container/whatever has changed name bc of the changes made to the docker compose. This is the updated command:
docker-compose run --rm website sh -c "python manage.py createsuperuser"

# To run program
Navigate to the /src folder.
Run docker compose up --build
When containers have launced, open Docker desktop and find the 'scheduler' container. It won't be running, so (re)start it. 
Click on the 'scheduler'-container and then click on the 'exec' tab. This opens a terminal within the container. Run this command to start the scheduler properly:
python scheduler.py

Wait 2 seconds, to ensure kafka connects properly
Program is now running. The terminal you've opened in Docker is also where we'll get the outputs about how long it took to process an order.