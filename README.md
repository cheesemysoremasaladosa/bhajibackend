# bhajibackend
The Backend for Bhajiwala Partner and Consumer

## Setup

- clone the repo and cd

    ``gh repo clone cheesemysoremasaladosa/bhajibackend && cd``

- create a virtual env

    ``python3 -m virtualenv .env``

- activate virtual env

    ``source .env/bin/activate``

- install package requirements

    ``pip install -r requirements.txt``

## Testing

currently the tests are placed in the `/tests` directory:

``
    pytest
``

## Running the server

* `fastapi dev app/main.py` : for local dev

* `fastapi dev app/main.py --host 0.0.0.0`: for use with apps

## API docs
`http://localhost:8000/docs`
