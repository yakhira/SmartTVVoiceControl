import time

def get_utc_timestamp(seconds=None):
    return time.strftime('%Y-%m-%dT%H:%M:%S.00Z', time.gmtime(seconds))


