# Resale Junction
* An Ecommerce website built on **Django** 
* Users can create their own profiles, post products for sale and buy other products listed on the website
* A **Stripe** payment gateway has also been integrated, which the users are redirected to on checkout
* The app also has been deployed on **AWS EC2**



## Tech Stack
* **Django** - Python Framework
* **TailwindCSS** - CSS Framework for styling 
* **Docker** - For containerization applications
* **AWS CLI** - For interacting with AWS Services
* **Amazon EC2** - Deployed app on Amazon EC2
* **Amazon S3** - Stored django artefacts on S3 and then pulled from EC2
* **Amazon ECR** - Repository for the docker image
* **Gunicorn** - Application Server used for Django
* **Nginx** - Web Server to handle web requests and serve static files

## Environment Variables
```
SECRET_KEY | For Django settings.py
STRIPE_PUBLIC_KEY
STRIPE_SECRET_KEY
```