# coding: utf-8
import json

import datetime
import requests
import urllib
import base64
import hmac

from hashlib import sha1
import time
import uuid

server_address = 'https://sms.aliyuncs.com'
access_key_id = 'xx'
access_key_secret = 'vvv'

# aliyun common api params
query_params = {
    'Format': 'JSON',
    'Version': '2016-09-27',
    'AccessKeyId': access_key_id,
    'SignatureVersion': '1.0',
    'SignatureMethod': 'HMAC-SHA1',
    'SignatureNonce': str(uuid.uuid1()),
    'RegionId': 'cn-hangzhou',
    'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time())),
}


def percent_encode(encode_str):
    encode_str = str(encode_str)
    res = urllib.quote(encode_str.decode('utf8').encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def compute_signature(params, secret):
    sorted_query_params = sorted(params.items(), key=lambda item: item[0])

    refine_query_string = ""
    for key, value in sorted_query_params:
        refine_query_string += "&" + percent_encode(key) + "=" + percent_encode(value)

    str_to_sign = 'GET&%2F&' + percent_encode(refine_query_string[1:])
    h = hmac.new(secret + "&", str_to_sign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature


def send_sms(phones, base_num, field_type, field_value,
             sms_sign='水质监测平台', sms_tpl='SMS_53900101'):
    user_settings = {
        'Action': 'SingleSendSms',
        'ParamString': json.dumps({
            'base_num': base_num,
            "field_type": field_type,
            "field_value": field_value,
            "time": datetime.datetime.now().strftime("%H:%M:%S")
        }),
        'RecNum': phones,
        'SignName': sms_sign,
        'TemplateCode': sms_tpl
    }

    query_params.update(user_settings)

    # compute signature
    query_params["Signature"] = compute_signature(query_params,
                                                  secret=access_key_secret)

    resp = requests.get(server_address, params=query_params)

    print "resp status_code %s" % resp.status_code
    print "resp content %s" % resp.json()
    return resp.status_code, resp.json()


if __name__ == "__main__":
    user_settings = {
        'Action': 'SingleSendSms',
        'ParamString': json.dumps({
            'base_num': "1809",
            "field_type": "溶解氧",
            "field_value": "10%",
            # "time": datetime.datetime.now().strftime("%H:%M:%S")
        }),
        'RecNum': '13299030795',
        'SignName': '天气预警',
        'TemplateCode': 'SMS_53740162'
    }
    query_params.update(user_settings)

    query_params["Signature"] = compute_signature(query_params,
                                                  secret=access_key_secret)

    resp = requests.get(server_address, params=query_params)

    print "resp status_code %s" % resp.status_code
    print "resp content %s" % resp.content

a.publish("exception_check",'{"base_num":1701, "check_field": ["S2"]}')