## JWT vs OAuth
#### JWT --> header.payload.signature
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
