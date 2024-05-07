# Token Bucket Python implementation

## Initialize the Class with required params
tb = TokenBucket(capacity=4, refill_rate=60, redis_host="127.0.0.1")

###capacity - number of request pass through within given refill_rate
###refill_rate - in seconds
###redis_host - localhost or cloud hosted path
###redis_port - default (6379)

## Call the get_token, return True if the request allowed otherwise false
tb.get_token(user_name="email_id")

or

tb.get_token(ip_add="20.21.333.1")

or 

tb.get_token("user_id", ",ip_add="20.21.333.1")