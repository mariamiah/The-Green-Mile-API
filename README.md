# The-Green-Mile-API
[![Build Status](https://travis-ci.org/mariamiah/The-Green-Mile-API.svg?branch=develop)](https://travis-ci.org/mariamiah/The-Green-Mile-API)

The Green-Mile is a web application that is meant for use in the door to door delivery of packages.

## Features
- Supplier can register/create their packages.
- Supplier can know the most efficient way the package will be delivered.
- The recepient can know when the package will arrive.
- Supplier can view their shipments.
- Supplier can view their invoices
- Recipient can receive packages
- Recipient can view deliveries
- The Admin is able to create, read, update and delete all information on the system.
- The loader is able to view information on how to load

## API Endpoints

| REQUEST | ROUTE                           | FUNCTIONALITY                 |
| ------- | ------------------------------- | ----------------------------- |
| POST    | api/v1/auth/login               | Logs in a user                |
| POST    | api/v1/auth/signup              | Registers a user              |
| GET     | api/v1/packages                 | Fetches all packages          |
| POST    | api/v1/packages                 | Supplier creates a package    |
| GET     | api/v1/packages/recipient_packages                    | Recipient can view their packages     |
| GET     | api/v1/packages/supplier_packages                     | Supplier can view packages they created |
| GET     | api/v1/packages/&lt;package_id>      | Fetches a single package |
| POST    | api/v1/status                   | Adds a shipment status        |
| POST    | api/v1/invoices                 | Creates an invoice            |
| POST    | api/v1/packages/loadingtype     | Creates the package loading type |
| POST    | api/v1/packages/packagetype     | Creates the package type      |
| GET     | api/v1/recipients               | Admin can view all recipients |
| GET     | api/v1/filter/<order_number>    | Filter all packages           |



### Getting started with the app

### Technologies used to build the application

-   [Python 3.6](https://docs.python.org/3/)
-   [Flask](http://flask.pocoo.org/)
-   [Postgres](http://postgresql.org/)

### Installation

Create a new directory and initialize git in it. Clone this repository by running

```sh
git clone https://github.com/mariamiah/The-Green-Mile-API.git
```

Create a virtual environment. For example, with virtualenv, create a virtual environment named venv using

```sh
virtualenv venv
```

Activate the virtual environment

```sh
cd venv/scripts/activate
```

Install the dependencies in the requirements.txt file using pip

```sh
pip install -r requirements.txt
```

Start the application by running

```sh
python run.py
```

Test your setup using [postman](www.getpostman.com) REST-client

### Running tests

-   Install nosetests
-   Navigate to project root
-   Use `nosetests tests/` to run the tests
-   To run tests with coverage, use `nosetests --with-coverage --cover-package=api && coverage report`

### View the API on heroku
- [greenmileapi](https://greenmileapi.herokuapp.com)


