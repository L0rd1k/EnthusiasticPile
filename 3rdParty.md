# JWT && OAuth
## JWT --> header.payload.signature
> #### 1. Header
``` javascript
{
   "alg": "HS256", # hashing algorithm being used, such as HMAC SHA256 or RSA.
   "typ": "JWT"    # the type of the token, which is JWT
}
```
> #### 2. Payload: Contains the claims(predefined keys and their values)
 There are three types of them:
- **Registered claims**: These are a set of predefined keys which are not mandatory but recommended. Some of them are iss (issuer), exp (expiration time) etc.
- **Public claims**: These can be defined by wish by those using JWTs. But to avoid collisions they should be defined in the IANA JSON Web Token Registry or be defined as a URI that contains a collision resistant namespace.
- **Private claims**: These are the custom key value pairs created to share information between parties that agree on using them and are neither registered or public claims.
 ``` javascript
{
   "exp": "2019-02-14",         # expiration time
   "message": "roses are red",
   # "sub": "1234567890",       # subject whome the token refers to)
   # "iat": 1516239022          # issued at(seconds since Unix epoch)
   
}
 ```
> #### 3. Signature:
To create the signature part you have to take the **encoded header**, the **encoded payload**, a **secret** - the algorithm specified in the header, and sign that. 
- **Signature** - verify that the sender of the JWT is who it says it is and to ensure that the message wasn't changed along the way.

### ** !!! IMPORTANT !!! ** 
- JWT tokens are used for authentication and not encryption, so even without knowing the secret key, someone can read our header and payload data.
- Don't store jwt in local storage(or session storage)
- Need to be stored inside *httpOnly* cookie ( cookie that's only sent in HTTP requests, and never accessible).

-----------------------------------------------------------------------------------------------------------------------
###  Authentication vs Authorization
> **Authentication** - process of verifying the identity of a user by obtaining some sort of credentials(password && login)
> **Authorization** - process of allowing an authenticated user to access his resources by checking permissions (whether the user has access rights to the system).


-----------------------------------------------------------------------------------------------------------------------
## 'OAuth' - open standart for authorization(protocol) with randomized tokens.
Works over HTTPS and authorize devices(API, servers, applications) with access tokens(not credentials).

#### 5 grants types for aquiring an access token:  
1. Authorization code grant:** flow redirects you to Log-in directly with 3rd party(client never gets access to our      login/password). 3rd party(Google, FaceBook, Twitter ant etc.) provider generates JWT for fetching data. Avoid necessity to provide our own account data and password.
2. Implicit grant
3. Resource owner credentials grant
4. Client credentials grant
5. Refresh token grant

#### OAuth2 uses HTTPS
1. Client  -----> Authorization Request  -----> Authorization Server(Google Server)
2. Client <-----  Authorization Grant   <-----  Authorization Server(Google Server)
3. Client  -----> Authorization Grant    -----> Authorization Server(Google Server)
4. Client <-----  Access Token && Refresh Token  <-----  Authorization Server(Google Server)
5. Client  ----->     Access Token       -----> Resource Server(Google Server)
6. Client <-----  Protected Resource    <-----  Resource Server(Google Server)

#### Types of Token
- **Access Token:** allows a 3rd party application to access user data on a resource server.
``` javascript
Example of sending an access token to the resource server using HTTP GET:
https://example.com/profile?access_token=MzJmNDc3M2VjMmQzN
```
- **Refresh Token:** this token is issued with the access token. But NOT sent in each request from the client to the resource server. The client application can simply use a refresh token to renew access token when it expires.
-----------------------------------------------------------------------------------------------------------------------

