# bhajibackend
The Backend for Bhajiwala Partner and Consumer

**NOTE: USE DOCKER METHOD TO AVOID HASSLES (NIKHIL, AYUSH, DEVANSH)**

## Setup

- clone the repo and cd

    ``gh repo clone cheesemysoremasaladosa/bhajibackend && cd``

- create a virtual env

    ``python3 -m virtualenv .env``

- activate virtual env

    ``source .env/bin/activate``

- install package requirements

    ``pip install -r requirements.txt``

- setup redis server on your machine

## Testing

currently the tests are placed in the `/tests` directory:

``
    pytest
``

## Running the server
> NOTE: start the redis server before running the following commands

* `fastapi dev app/main.py` : for local dev

* `fastapi dev app/main.py --host 0.0.0.0`: for use with apps


## Alernative: Docker

> **NOTE** Ensure docker/docker desktop is setup on the system

- clone the repo and cd

    ``gh repo clone cheesemysoremasaladosa/bhajibackend && cd``

- build containers
	`sudo docker compose build`

- start the containers
	`sudo docker compose up`	

## API docs
`http://localhost:8000/docs`
