# Setup

## In a container

load the image tar to the local repository:

> docker load -i health_check.tar

run the server mapped to port 5000:

> docker run -p 5000:5000 health_check

at this point the server should be running in a container listening to local port 5000

## Locally

pull the project from github:

> git pull https://github.com/geco333/longevity_assignment.git

create a python virtual environment:

> python -m venv venv

install all dependencies:

> pip install -r requirements.txt

run the flask server:

> flask run

the server should now be available locally (port 5000 by default)

# Structure and logic

## Database

the project uses SQLite, by default the db file and all tables will be initialized as part of the flask server setup.

when running as a docker container the database is volatile and all data will be lost once the container stops.

## Endpoints

### ***/users***

- **GET**: returns a list of all the users.


- **POST**: create a new user, payload example:
  ```
  {
      "username": "Jayanti Riderch",
      "email": "JRiderch@gmail.com",
      "gender": "female",
      "age": "58"
  }
  ```

### ***/users/{user_id}***

- **GET**: returns all data relating to the `user_id` provided.


- **PUT**: update user information, payload example:
  ```
  {
      "username": "Eliezer Nanaia",
      "email": "ENanaia@gmail.com",
      "gender": "male",
      "age": "77"
  }
  ```

- **DELETE**: removes an existing user.

### ***/users/{user_id}/{activity}***

- **GET**: returns all `activity` data relating to the `user_id` provided.
  possible `activity` values:
    - physical
    - sleep


- **POST**: create new `activity` information for the `user_id` provided, example:
  ```
  localhost:5000/users/3/physical
  
  {
      "exercising_hours": 7,
      "steps": 2100,
      "km": 5
  }
  ```

- **PUT**: update `activity` information, payload example:
  ```
  localhost:5000/users/12/sleep
  
  {
      "total_hours": 7,
      "wake_ups": 2
  }
  ```

- **DELETE**: removes an `activity` for the provided `user_id`.

### ***/users/{user_id}/blood***

- **GET**: returns all blood test data relating to the `user_id` provided.


- **POST**: create a new blood test entry for the `user_id` provided, payload example:
  ```
  {
      "cbc": 7,
      "wbc": 21,
      "rbc": 50,
      "hct": 2,
      "hgt": 211
  }
  ```

### ***/users/{user_id}/get_health_score***

- **GET**: calculates and returns the health score for the provided `user_id`.
  health score is the combined average of all physical activity parameters out of
  the total sum of all values for a given parameter:

> ({users exercising_hours} / {total exercising_hours}) + ({user steps} / {total steps}) + ({user km} + {total km})

### ***/{activity}***

- **GET**: returns a list of all entries of the given `activity` in the database. possible `activity` values:
    - *physical*
    - *sleep*

### ***/{activity}/{activity_id}***

- **GET**: returns all information of the given `activity` relating to the given `activity_id`.


- **PUT**: updates an existing `activity` entry, example:
  ```
  localhost:5000/sleep/7
  
  {
      "total_hours": 6,
      "wake_ups": 0
  }
  ```

- **DELETE**: removes the `activity_id` entry for the given `activity`.

### ***/blood***

- **GET**: returns a list of all blood test entries in the database.

### ***/blood/{blood_test_id}***

- **GET**: returns all blood test information for to the given `blood_test_id`.


- **PUT**: updates an existing blood test provided in `blood_test_id`, example:
  ```
  localhost:5000/blood/19
  
  {
      "cbc": 16,
      "hct": 900
  }
  ```

- **DELETE**: removes a blood test entry from the database. 

