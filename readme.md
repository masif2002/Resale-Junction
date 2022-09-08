# buyNsell
An Ecommerce website built using **Django**. The frontend aspect of the app is styled using **tailwindcss**. Users can create their own profiles, post products for sale and buy the products listed on the website. A **stripe payment gateway** has also been integrated, which the users are redirected to on checkout

## Tech Stack
* **Django** - Python Framework
* **TailwindCSS** - CSS Framework
* **Docker** - For containerization
* **AWS CLI** - For interacting with AWS Services
* **Amazon EC2** - Deployed app on Amazon EC2
* **Amazon S3** - Stored django artefacts on S3 and then pulled from EC2
* **Amazon ECR** - Repository for the docker image
* **Gunicorn** - Application Server used for Django
* **Nginx** - Web Server to handle web requests and serve static files