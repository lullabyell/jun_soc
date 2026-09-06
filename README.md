# Junior SOC API Assessment

A minimal FastAPI authentication API created as part of a Junior SOC assessment.

The API implements:

* User login with username and password
* Argon2 password hashing
* JWT access and refresh tokens
* Protected `/profile` endpoint
* Refresh token flow
* Basic input validation
* Environment-based JWT secret configuration

## Technologies

* Python 3.11+
* FastAPI
* PyJWT
* pwdlib with Argon2
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

### 1. Install dependencies

Make sure Poetry is installed, then run:

```bash
poetry install
```

### 2. Configure environment variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Generate a random JWT secret:

```bash
openssl rand -hex 32
```

Put the generated value in `.env`:

```text
JWT_SECRET_KEY=your-generated-secret
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

The `.env` file is excluded from Git and should not be committed.

## Running the API

Start the development server with:

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### `GET /health`

Checks whether the API is running.

Example response:

```json
{
  "status": "ok"
}
```

### `POST /login`

Authenticates a user and returns an access token and refresh token.

Example request:

```json
{
  "username": "aidana",
  "password": "testpassword"
}
```

Example response:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

### `GET /profile`

Returns information about the authenticated user.

The access token must be provided using the `Authorization` header:

```text
Authorization: Bearer <access_token>
```

### `POST /refresh`

Accepts a valid refresh token and returns a new access token.

Example request:

```json
{
  "refresh_token": "<refresh_token>"
}
```

## Testing

Run the automated tests with:

```bash
poetry run pytest
```

The tests cover successful and failed login attempts, protected profile access, refresh tokens, and preventing refresh tokens from being used as access tokens.

## Security

The application includes several basic security controls:

* Passwords are hashed using Argon2.
* JWT decoding explicitly allows only the `HS256` algorithm.
* Access tokens have a short lifetime of 15 minutes.
* Refresh tokens have a 7-day lifetime.
* Access and refresh tokens have different token types.
* JWT secrets are loaded from environment variables.
* `.env` is excluded from Git.
* Login errors use a generic message to reduce username enumeration.

The main identified limitation is the absence of rate limiting or account lockout for repeated failed login attempts.

Additional security analysis, including JWT `alg:none` testing, brute-force testing, and command-line log analysis, is documented in [`SECURITY_REVIEW.md`](SECURITY_REVIEW.md).

## Assessment Notes

This project intentionally uses an in-memory user store and does not use a database. This keeps the implementation minimal for the assessment but would not be appropriate for a production authentication system without additional infrastructure and security controls.
