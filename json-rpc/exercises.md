# JSON-RPC Exercises

1. Implement a server for a JSON-RPC service that registers a user by means of a "register" API function accepting a username and a password as a parameter. The function will return 0 if the user could be successfully registered or 1 if the user already exists.
2. Implement a function "login" that accepts a username and a password and returns a 40-byte Base64 token if username and password are correct, or the string "Unknown user" otherwise.
3. Implement a function "is_token_valid" that accepts a username and a token and returns 1 if the token is currently valid, or 0 otherwise.
4. Implement a function "logout" that accepts a username and a token and invalidates the token given as a parameter.