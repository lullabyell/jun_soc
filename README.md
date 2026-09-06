# SOC API Assessment

This is a small FastAPI project made for a SOC assessment.

The API has a simple authentication system with:

* Login with username and password
* Password hashing with Argon2
* JWT access and refresh tokens
* Protected `/profile` endpoint
* Refresh token endpoint
* Basic input validation
* JWT secret stored in environment variables

## Technologies

* Python
* FastAPI
* PyJWT
* pwdlib / Argon2
* python-dotenv
* Poetry
* pytest

## Project Structure

```text
jun_soc/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── main.py
│   ├── models.py
│   └── users.py
├── logs/
│   └── access.log
├── tests/
│   └── test_auth.py
├── .env.example
├── .gitignore
├── README.md
├── SECURITY_REVIEW.md
├── poetry.lock
└── pyproject.toml
```

## Setup

First install the dependencies:

```bash
poetry install
```

Create a `.env` file:

```bash
cp .env.example .env
```

Then add a random secret to the `.env` file. For example:

```bash
openssl rand -hex 32
```

The `.env` file should not be committed to Git.

Example:

```text
JWT_SECRET_KEY=generated-secret
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Running the API

Start the application with:

```bash
poetry run uvicorn app.main:app --reload
```

The API will run on:

```text
http://127.0.0.1:8000
```

FastAPI also provides interactive documentation at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### `GET /health`

Checks if the API is running.

Example response:

```json
{
  "status": "ok"
}
```

### `POST /login`

Used to log in with a username and password.

Example:

```json
{
  "username": "aidana",
  "password": "testpassword"
}
```

If the credentials are correct, the API returns an access token and a refresh token.

### `GET /profile`

Returns information about the logged-in user.

An access token is required:

```text
Authorization: Bearer <access_token>
```

### `POST /refresh`

Used to get a new access token using a refresh token.

Example:

```json
{
  "refresh_token": "<refresh_token>"
}
```

## Testing

Run the tests with:

```bash
poetry run pytest
```

The tests check things like:

* Successful login
* Wrong password
* Accessing `/profile` without a token
* Accessing `/profile` with a valid token
* Refreshing a token
* Making sure a refresh token cannot be used as an access token

## Security

Some basic security measures were added:

* Passwords are stored as Argon2 hashes.
* JWTs only accept the `HS256` algorithm.
* Access tokens expire after 15 minutes.
* Refresh tokens expire after 7 days.
* Access and refresh tokens have different types.
* The JWT secret is stored in `.env`.
* `.env` is included in `.gitignore`.
* Failed login attempts return a general error message.

One limitation is that there is currently no rate limiting for repeated login attempts.

More details about the security testing and log analysis can be found in [`SECURITY_REVIEW.md`](SECURITY_REVIEW.md).

## Notes

The users are stored in memory instead of a database. I used this approach to keep the project small and focused on the requirements of the assessment.

For a real application, a database and additional security controls would be needed.
