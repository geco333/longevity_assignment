# Usage
## In a container

load the image tar to the local repository:

> docker load -i health_check.tar

run the server mapped to port 5000:

> docker run -p 5000:5000 health_check

at this point the server should be running in a container listening to port 5000  

## Locally

pull the project from github:

> git pull 