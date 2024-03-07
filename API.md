# API Documentation

**URL** : http://localhost:80/


Summary:
  * [User Registration](#1-user-registration) - `POST /api/register/`
  * [User Login](#2-user-login) - `POST /api/login/`
  * [User Profile Information](#3-user-profile-information) - `GET /api/profile/`
  * [42 OAuth2](#4-42-oauth2) - `GET /api/auth/42/`

------------------------------------------------------------------------------------------------------------------
### 1. User Registration

- **HTTP Method:** `POST`
- **PATH:** `/api/register/`
- **Permissions:** All (unauthenticated)
- **Description:** Allows a user to register with an email, username and password.

#### Request Parameters

```json
{
  "email": "user@gmail.com",
  "username": "user",
  "password": "password"
}
```

####  Response
###### <span style="color:green">Success</span>
Status code : 201

```json
{
  "id": 1,
  "username": "user",
  "email": "user@gmail.com",
  "profile_image": "backend/profile_images/default.jpg"
}
```

------------------------------------------------------------------------------------------------------------------

### 2. User Login

- **HTTP Method:** `POST`
- **PATH:** `/api/login/`
- **Permissions:** All (unauthenticated)
- **Description:** Allows an existing user to log in and obtain a JWT authentication token.

#### Request Parameters

```json
{
  "username": "user",
  "password": "password"
}
```

#### Response

###### <span style="color:green">Success</span>

Status code : 200

```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "user",
    "email": "user@gmail.com",
    "profile_image": "backend/profile_images/default.jpg"
  }
}
```

###### <span style="color:red">Error</span>

Status code: 400
```json
{
  "error_message": "Invalid username or password"
}
```

------------------------------------------------------------------------------------------------------------------

###### <span style="color:red">For all the following endpoints, the user must be authenticated and provide the JWT token in the header.</span>
```json
headers: {
    "Authorization": `Bearer ${localStorage.getItem("accessToken")}`,
  }
```

##### <span style="color:red">If the token is expired, the user must refresh it using the refresh token provided in the login response by doing something like this:</span>
```js
async function refreshToken() {
    try {
        const response = await fetch(apiUrl + 'token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (response.ok) {
            const tokens = await response.json();
            // Update the access token for future requests
            accessToken = tokens.access;
            console.log('New Access Token:', accessToken);
        } else {
            console.error('Token refresh failed:', response.statusText);
        }
    } catch (error) {
        console.error('Error during token refresh:', error);
    }
}
```

### 3. User Profile Information

- **HTTP Method:** `GET`
- **PATH:** `/api/profile/`
- **Permissions:** Authenticated
- **Description:** Returns the profile information of the authenticated user.

#### Response

###### <span style="color:green">Success</span>

Status code : 200

```json
{
  "id": 1,
  "username": "user",
  "email": "user@gmail.com",
  "profile_image": "backend/profile_images/default.jpg"
}
```

------------------------------------------------------------------------------------------------------------------

### 4. 42 OAuth2

- **HTTP Method:** `GET`
- **PATH:** `/api/auth/42/`
- **Permissions:** All (unauthenticated)
- **Description:** Redirects the user to the 42 OAuth2 authentication page.

#### Response

###### <span style="color:green">Success</span>
Status code : 200

```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "user",
    "email": "user@gmail.com",
    "profile_image": "backend/profile_images/default.jpg"
  }
}
```