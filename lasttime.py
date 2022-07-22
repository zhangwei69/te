import datetime
import time
print(time.strftime("%Y-%m-%d",time.localtime(time.time())))
print(datetime.date.today())
now_time = datetime.datetime.now()
end_time = now_time + datetime.timedelta(days = -1)
# 前一天时间只保留 年-月-日
enddate = end_time.strftime('%Y-%m-%d') #格式化输出
print(enddate == time.strftime("%Y-%m-%d",time.localtime(time.time())))