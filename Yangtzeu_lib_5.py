# 导入所需库：
import time
import json
import requests
from selenium import webdriver
from time import localtime as tm

# 个人信息与预约信息字典
with open('./Lib/users_dict.dll', 'r', encoding='utf-8') as f:
    users = eval(f.read())  # 账密字典
with open('./Lib/data_dict.dll', 'r', encoding='utf-8') as d:
    data_dict = eval(d.read())

login_url = 'https://cas.yangtzeu.edu.cn/authserver/login?service=https%3A%2F%2Fseat.yangtzeu.edu.cn%2Fremote%2Fstatic%2FcasAuth%2FgetServiceByVerifyTicket%2FcasLogin'

# 填写日期
def choice_date():
    if tm().tm_hour >= 21:  # 21点+运行则选择次日，否则默认为当日
        date_num = tm().tm_mday + 1
    else:
        date_num = tm().tm_mday
    return date_num

# 创建浏览器对象并打开目标网站：
def start_driver(url):
    print('打开登录界面...')
    opt = webdriver.EdgeOptions()
    opt.add_argument('--no-sandbox')
    opt.add_argument('lang=zh_CN.utf-8')
    opt.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
    opt.add_argument('window-size=1920x3000')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--disable-infobars')
    opt.add_argument('--hide-scrollbars')
    opt.add_argument('blink-settings=imagesEnabled=false')
    opt.add_argument('--headless')
    driver = webdriver.Edge('./msedgedriver.exe', options=opt)   # 创建Edge浏览器对象
    driver.implicitly_wait(30)  # 隐式等待
    driver.get(url)
    return driver

# 找到账号和密码的输入框，输入账号、密码并提交：
def input_Account(driver, users):
    print('登录...')
    driver.find_element('id', value='username').send_keys(users['Id'])  # 找到账号输入框并输入
    driver.find_element('id', value='password').send_keys(users['passwd'])  # 找到密码输入框并输入
    driver.find_element('id', value='login_submit').click()  # 提交
    time.sleep(3)  # 等待3秒，避免页面还没加载完
    return driver

# 登录
def login_in(url, users):
    driver = start_driver(url=url)
    driver = input_Account(driver=driver, users=users)
    print('获取cookie...')
    cookies = driver.get_cookies()
    driver.quit()
    with open('./Lib/cookies.dll', 'w', encoding='utf-8') as f:
            f.write(str(cookies))
    print('已获取cookie...')

# 尝试登录
def try_login():
    count = 0
    while count <= 10:
        try:
            login_in(url=login_url, users=users)
            break
        except:
            print(f'失败{count + 1}次...')
            time.sleep(30)
            count += 1
            continue

# 等待并保持访问...：
def wait_time(headers):
    print('等待...')
    # 设置cookies
    with open('./Lib/cookies.dll', 'r', encoding='utf-8') as f:
        cookies = eval(f.read())
        ID = cookies[2]['value']
    sess = requests.Session()
    for cookie in cookies:
        sess.cookies.set(name=cookie['name'], value=cookie['value'])

    while tm().tm_hour == 21 and tm().tm_min <= 37:  # 21:37以前每两分钟刷新一次
        time.sleep(30)
        print('刷新cookie...')
        sess.get(url=f'http://seat.yangtzeu.edu.cn/libseat-ibeacon/nowActivity;jsessionid={ID}', headers=headers)
    return sess

# 计算时间Id
def get_time(start_time, end_time):
    start_time_hour = int(start_time)
    end_time_hour = int(end_time)
    if (float(start_time) - start_time_hour) == 0:
        start_num = start_time_hour * 60
    else:
        start_num = start_time_hour * 60 + 30
    if (float(end_time) - end_time_hour) == 0:
        end_num = end_time_hour * 60
    else:
        end_num = end_time_hour * 60 + 30
    return start_num, end_num

# 发送预约请求
def get_seat(roomId, seatId, start_num, end_num, date_num=tm().tm_mday):
    year = tm().tm_year
    month = '%02d' % tm().tm_mon

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Host": "seat.yangtzeu.edu.cn",
        "Referer": f"http://seat.yangtzeu.edu.cn/libseat-ibeacon/seatdetail?linkSign=activitySeat&roomId={roomId}&date={year}-{month}-{date_num}&buildId=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
        "X-Requested-With": "XMLHttpRequest"
    }

    sess = wait_time(headers=headers)
    while tm().tm_hour == 21 and tm().tm_min < 40:
        time.sleep(1)
    print(f'尝试预约时间: %02d:%02d' % (tm().tm_hour, tm().tm_min))
    for i in range(10):
        try:
            res = sess.get(url=f'http://seat.yangtzeu.edu.cn/libseat-ibeacon/saveBook?seatId={seatId}&date={year}-{month}-{date_num}&start={start_num}&end={end_num}&type=1&captchaToken=', headers=headers)
        except:
            continue
        res.encoding = res.apparent_encoding
        with open('./Lib/res.txt', 'w+', encoding='utf-8') as f:
            f.write(res.text)
        res = json.loads(res.text)
        res = json.loads(res)
        status = res['status']
        if status == 'success':   
            return res
        else:
            if i != 9:
                print(f'失败第{i + 1}次...')
                continue
            else:
                print('失败共10次, 返回失败结果...')
                return res
            
# 尝试点击
def try_click(driver, submit):
    try:
        submit.click()
    except:
        try:
            driver.execute_script('arguments[0].click();', submit)
        except:
            print(f'尝试点击"{submit}"出错...')
    return driver

# 结果输出函数
def print_result(users, status, onDate=0, begin=0, end=0, location=0, message=None):
    print('-' * 50)
    print('Id: ', users['Id'])
    if status == 'success':
        print('onDate: ', onDate)
        print('location:', location)
        print('begin: ', begin)
        print('end: ', end)
    else:
        print(message)
        print('Failed!!!')
    print('-' * 50)

# 主函数
def main(event=False):
    date_num = choice_date()
    start_num, end_num = get_time(start_time=data_dict['start_time'], end_time=data_dict['end_time'])
    if event == False:
        try_login()
    res = get_seat(roomId=data_dict['roomId'], seatId=data_dict['seatId'], start_num=start_num, end_num=end_num, date_num=date_num)
    status = res['status']
    if status == 'success':
        data = res['data']
        print_result(users, status=status, onDate=data['onDate'], begin=data['begin'], end=data['end'], location=data['location'])
    else:
        print_result(users, status=status, message=res['message'])


# 主程序入口
if __name__ == '__main__':
    while tm().tm_hour < 21 and tm().tm_hour > 18:
        time.sleep(60)
    while tm().tm_hour ==21 and tm().tm_min < 30:
        print('等待...')
        time.sleep(60)
    try:
        main(event=False)
    except Exception as E:
        print(E)
        main(event=True)
    while True:
        time.sleep(300)