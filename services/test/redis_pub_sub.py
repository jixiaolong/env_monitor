import redis


con = redis.Redis()
con.publish("exception_check", {
    "base_num": "1809",
    "check_field": ["S2"]
})
