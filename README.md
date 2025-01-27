## Start

Start the application with:

`docker compose up --build`

The application is running on http://localhost:8000 and is loaded with fixtures.

Superuser credentials are:
- username: `root`
- password: `Test_password1`

Swagger technical documentation is available on `/docs`.

## Test

With the django container running, automatic testing can be launched with: 

`docker exec django pytest`

OR 

enter the container with:

`docker exec -it django bash`

once inside the container:

`pytest`