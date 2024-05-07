### Token Bucket Python Implementation
This Python class provides a token bucket algorithm implementation for rate limiting requests. It allows you to initialize the class with the required parameters and then check if a request should be allowed based on the token availability.

### Usage
Initialize the class with the required parameters:

```python
Copy code
tb = TokenBucket(capacity=4, refill_rate=60, redis_host="127.0.0.1", redis_port=6379)
```

| Parameter     | Description                                           |
|---------------|-------------------------------------------------------|
| `capacity`    | The maximum number of requests allowed.               |
| `refill_rate` | The time interval (in seconds) for token refilling.   |
| `redis_host`  | The host address of the Redis server.                 |
| `redis_port`  | The port number of the Redis server (default is 6379).|


```python
Copy code
# For logged-in users
tb.get_token(user_name="email_id")

# For anonymous users by IP address
tb.get_token(ip_add="20.21.333.1")

# For a combination of user_id and IP address
tb.get_token(user_id="user_id", ip_add="20.21.333.1")
```

The get_token method returns True if the request is allowed within the rate limit, otherwise False.

### Note: This class accepts two parameters: user_id for logged-in users and ip_add for anonymous users.