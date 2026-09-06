# Security Review

## 1. Self-Audit

### Security controls

I added the following security controls to the API.

**1. Passwords are hashed with Argon2**

Passwords are not stored directly. They are stored as Argon2 hashes.

I used Argon2 because it is made for password hashing.

**2. JWT algorithm is restricted**

The API uses `HS256` for signing JWTs.

When decoding a token, the application only allows `HS256`. This means that a token using another algorithm, such as `none`, is rejected.

**3. Access and refresh tokens are separated**

Access tokens expire after 15 minutes.

Refresh tokens expire after 7 days.

The tokens also have different `type` values. Because of this, a refresh token cannot be used to access `/profile`.

**4. JWT secret is not stored in the code**

The JWT secret is loaded from the `.env` file.

The `.env` file is included in `.gitignore`, so it should not be committed to Git.

The repository only contains `.env.example` with a placeholder value.

**5. Login errors are general**

When login fails, the API returns:

```text
Invalid username or password
```

The API does not say whether the username exists. This gives an attacker less information when trying different usernames.

### Limitations

The user data is stored in memory, so this is not suitable for a real production application.

Another limitation is that refresh tokens are not rotated. The same refresh token can be used again until it expires.

I kept these parts simple because this is a small assessment project.

---

## 2. JWT `alg:none` Test

### What I tested

I wanted to check if the API would accept a JWT where the algorithm is changed to `none`.

I changed the JWT header to:

```json
{
  "alg": "none",
  "typ": "JWT"
}
```

Then I used the modified token to access:

```text
GET /profile
```

### Result

The API returned:

```text
401 Unauthorized
```

So the token was rejected.

The JWT decoding code only allows `HS256`:

```python
jwt.decode(
    token,
    JWT_SECRET_KEY,
    algorithms=[JWT_ALGORITHM],
)
```

This prevents the API from accepting a token with the `none` algorithm.

### Conclusion

The test passed because the modified token was rejected.

---

## 3. Brute-Force Login Test

### What I tested

I tested what happens if someone sends many incorrect passwords to:

```text
POST /login
```

I sent multiple login attempts with incorrect passwords.

The API returned `401 Unauthorized` for the failed attempts. After that, a login with the correct password was successful.

### Result

The API handles incorrect passwords correctly, but there is currently no rate limiting or account lockout.

This means someone could keep trying passwords many times.

### Risk

An attacker could use many login attempts to try to guess a user's password.

### Possible improvement

For a real application, I would add rate limiting and monitoring for repeated failed login attempts.

---

## 4. Log Analysis

For the log analysis, I used the sample log file in:

```text
logs/access.log
```

The log file contains test data created for this assessment.

### Finding failed login attempts

I used:

```bash
grep "POST /login 401" logs/access.log | awk '{print $3}' | sort | uniq -c | sort -nr
```

The result was:

```text
20 192.168.1.25
3 203.0.113.45
```

The IP `192.168.1.25` had the most failed login attempts.

### Checking successful logins

I used:

```bash
grep "POST /login 200" logs/access.log
```

One of the results was:

```text
2026-09-06 16:51:30 192.168.1.25 POST /login 200
```

### Checking the suspicious IP

I then checked all activity from this IP:

```bash
grep "192.168.1.25" logs/access.log
```

The activity showed:

* 20 failed login attempts in a short period
* A successful login immediately after the failed attempts
* A successful `/profile` request after the login

This looks suspicious because there were many failed attempts followed by a successful login.

### SOC assessment

I would consider `192.168.1.25` a possible brute-force or password-guessing attempt.

The logs alone do not prove that the account was compromised. I would need more information, such as the username and other logs, to investigate it further.

The activity from `203.0.113.45` also contains failed and successful logins, but there were only three failed attempts, so it looks less suspicious.

---

## 5. Other Security Considerations

### Token storage

The API creates the tokens, but how the client stores them is not part of this project.

For example, storing tokens in `localStorage` could be a problem if a website has an XSS vulnerability.

For a real application, I would look into using secure HttpOnly cookies or another secure token storage method.

### SQL Injection

This project does not use a database, so there are currently no SQL queries to attack.

If a database was added later, I would use parameterized queries or an ORM instead of building SQL queries directly from user input.

---

## 6. Conclusion

The API implements the main authentication requirements and has some basic security protections.

I tested the JWT `alg:none` case and the token was rejected.

I also tested repeated login attempts. The main weakness I found is that there is no rate limiting, so an attacker could continue trying passwords.

The project is intentionally small and does not include a database or production-level security features.
