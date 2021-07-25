from datetime import datetime, timedelta, timezone
seoul_timezone = timezone(timedelta(hours=9), 'Asia/Seoul')


def request_url(resource):
    baseUrl = 'https://www.thecamp.or.kr'
    r = "{}/{}".format(baseUrl, resource)
    return r


def get_kr_now():
    return datetime.now(tz=timezone.utc).astimezone(tz=seoul_timezone)
