import hashlib
import time
import redis


class TokenBucket:
    """
    A bucket of tokens which can be used for a given time interval

    The Bucket is self refilling and can tell how much tokens we can use.
    """

    def __init__(self, capacity, refill_rate, redis_host=None, redis_port=6379) -> None:
        """
        Initializes the token bucket

        Parameters
        ---------------------------
        capacity: Int
            maximum no of token in the bucket

        refill_rate: Int ( in seconds)
            No of seconds after which the bucket refilled

        redis_host: hostname
            Redis host details to manage the token entires
        """

        self.capacity = capacity
        self.refill_rate = refill_rate
        self.redis = redis.Redis(host=redis_host, port=redis_port)

    def generate_key(self, user_name=None, ip_add=None):
        if not user_name and not ip_add:
            return False

        keys = []
        if user_name:
            keys = [user_name]
        if ip_add:
            keys.append(hashlib.sha256(ip_add.encode()).hexdigest())
        return ":".join(keys)

    def get_token(self, user_name=None, ip_add=None):
        key = self.generate_key(user_name, ip_add)
        current_time = time.time()

        data = self.redis.hgetall(key)
        tokens = int(data.get(b"tokens", self.capacity))
        last_refill_time = data.get(b"last_refill_time")

        if last_refill_time:
            last_refill_time = float(last_refill_time)
        else:
            last_refill_time = current_time

        time_difference = current_time - last_refill_time
        if time_difference == 0:
            last_refill_time = current_time
        elif time_difference > 0:
            if time_difference > self.refill_rate:
                # Reset the tokens
                self.redis.hset(
                    key, mapping={"tokens": self.capacity -1,"last_refill_time": current_time}
                )
                return True
        self.redis.hset(
            key, mapping={
                "tokens": tokens - 1, "last_refill_time": last_refill_time
            }
        )
        if tokens > 0:
            return True
        return False

    def limit(self, func):
        """
        This function act as a decorator we can use this with python classes / api functions
        """

        def wrapper(*args, **kwargs):
            user_name = kwargs.get("user_name")
            ip_address = kwargs.get("ip_address")
            if self.get_token(user_name, ip_address):
                return func(*args, **kwargs)
            else:
                raise Exception("429 Too many requests")

        return wrapper
