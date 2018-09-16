from django import template

# 转化为清醒时间
from datetime import datetime
from django.utils.timezone import now as now_func
# 导入服务器本地时间,settings中设置的TIME_ZONE = 'Asia/Shanghai'
from django.utils.timezone import localtime

register=template.Library()
@register.filter
def time_since(value):
    if not isinstance(value,datetime):
        return value
    # 当前的清醒时间
    now=now_func()
    timestamp=(now - value).total_seconds()
    if timestamp < 60:
        return '刚刚'
    elif timestamp >= 60 and timestamp < 60*60:
        minutes=int(timestamp/60)
        return '%s分钟前'%minutes
    elif timestamp >=60*60 and timestamp <60*60*24:
        hours=int(timestamp/60/60)
        return  '%s小时前'%hours
    elif timestamp >=60*60*24 and timestamp <60*60*24*30:
        days=int(timestamp/60/60/24)
        return '%s天前'%days
    else:
        return value.strftime('%Y-%m-%d %H:%m')

@register.filter
def pub_times(value):
    # 如果传入值的格式不是datetime格式，那么就原值返回
    if not isinstance(value,datetime):
        return value
    return localtime(value).strftime('%Y-%m-%d %H:%m:%S')


