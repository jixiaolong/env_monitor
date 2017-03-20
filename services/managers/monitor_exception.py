# -*- coding:utf-8 -*-
import json
import os

import datetime, time
import redis

import dataset
import yaml
import sys

sys.path[0] = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


from sms import send_sms


db_setting = {
    "host": "127.0.0.1",
    "port": "3306",
    "db_name": "env_monitor_beinong",
    "user": "root",
    "password": "long12345"
}

settings = yaml.load(open("check_principle.yml"))


def update_map(base_num_field):
    """ update the map between base_num and the last request time
    :param base_num:
    :return:
    """
    no_db = redis.Redis()
    request_time = time.mktime(datetime.datetime.now().timetuple())
    print "base_num_field %s " % base_num_field
    print "request_time %s " % request_time

    no_db.set(base_num_field, request_time)


def get_db_object(table_name, base_num):
    db = dataset.connect("msyql://{user}:{password}@{host}:/{db_name}".format(
        user=db_setting["user"],
        password=db_setting["password"],
        host=db_setting["host"],
        db_name=db_setting["db_name"]
    ))
    object_dict = db[table_name].find_one(base_num=base_num, order_by="-id")
    db.close()
    return object_dict


def trigger_check(data):
    if not isinstance(data, basestring):
        print "data format is not right"

    msg = json.loads(data)
    base_num = msg["base_num"]
    check_field = msg["check_field"]

    base_data = get_db_object("models_basedata", base_num)
    base_info = settings[msg["base_num"]]
    for field in check_field:
        field_value = base_data[field]

        check_value = base_info[field]["check_value"]
        field_type = base_info[field]["name"]
        human_value = "%s%s" % (check_value, base_info[field]["unit"])
        phones = base_info["phones"].join(",")

        if check_value < field_value and phones and human_value and field_type:
            redis_check_key = "{base_num}->field:{field}".format(
                base_num=msg["base_num"],
                field=field
            )
            no_db = redis.Redis()
            last_info = no_db.get(redis_check_key, 0)
            if last_info:
                now_time = time.mktime(datetime.datetime.now().timetuple())
                last_request_time = float(last_info)
                if last_request_time + 60*60 > now_time:
                    print "time too short && pass it"
                    continue

            http_status_code, msg = send_sms(phones,
                     msg["base_num"],
                     field_type,
                     human_value,
                     sms_sign="天气预警",
                     sms_tpl="SMS_53740162")

            if http_status_code == 200:
                request_time = time.mktime(datetime.datetime.now().timetuple())
                no_db.set(redis_check_key, request_time)
                print "update ok"


def get_notify(channel):
    con_pool = redis.client.ConnectionPool()
    sub = redis.client.PubSub(con_pool)

    sub.subscribe(channel)

    while True:
        try:
            for msg in sub.listen():
                trigger_check(msg.get("data"))
        except:
            pass


if __name__ == "__main__":
    get_notify("exception_check")

