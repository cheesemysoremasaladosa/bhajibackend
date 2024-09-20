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

currently the test's are placed in the `app/` directory:

``
    pytest
``

## Running the server

* `fastapi dev main.py` : for local dev

* `fastapi dev main.py --host 0.0.0.0`: for use with apps

## API docs
`http://localhost:8000/redoc`