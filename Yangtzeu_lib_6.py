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
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44'}

# 填写日期
def choice_date():
    if tm().tm_hour >= 21:  # 21点+运行则选择次日，否则默认为当日
        date_num = tm().tm_mday + 1
    else:
        date_num = tm().tm_mday
    return date_num

# 创建无头浏览器对象并打开目标网站：
def start_driver(url):
    # 创建无头浏览器并设置参数
    print('创建浏览器...')
    driver = webdriver.Edge()   # 创建Edge浏览器对象
    driver.implicitly_wait(30)  # 隐式等待
    print('浏览器设置完成...')

    # 打开登录界面
    print('打开登录界面...')
    driver.get(url)
    print('登录界面已打开...')
    return driver

# 找到账号和密码的输入框，输入账号、密码并提交：
def input_Account(driver, users):
    print('输入帐密...')
    driver.find_element('id', value='username').send_keys(users['Id'])  # 找到账号输入框并输入
    driver.find_element('id', value='password').send_keys(users['passwd'])  # 找到密码输入框并输入
    driver.find_element('id', value='login_submit').click()  # 提交
    time.sleep(3)  # 等待3秒，避免页面还没加载完
    return driver

# 登录
def login_in(url, users):
    # 进行登录操作
    print('登陆操作...')
    driver = start_driver(url=url)
    driver = input_Account(driver=driver, users=users)
    print('登录成功...')

    # 记录登录时间戳
    with open('./Lib/login_time.dll', 'w', encoding='utf-8') as n_t:
        print('记录登录时间戳...')
        n_t.write(str(int(time.time())))

    # 获取cookie并关闭浏览器
    print('获取cookie...')
    cookies = driver.get_cookies()
    print('已获取cookie...')
    print('关闭浏览器...')
    driver.quit()
    print('浏览器已关闭...')

    # 本地化cookie
    print('本地化cookie...')
    with open('./Lib/cookies.dll', 'w', encoding='utf-8') as f:
            f.write(str(cookies))
    print('本地化cookie已完成...')

# 尝试登录
def try_login():
    count = 0
    while count <= 10:
        if requests.get(login_url, stream=True, verify=False).status_code != 404:
            try:
                login_in(url=login_url, users=users)
                break
            except:
                print(f'登录失败{count + 1}次...')
                time.sleep(30)
                count += 1
                continue
        else:
            print('404')
            time.sleep(30)

# 等待并保持访问...：
def wait_time(headers):
    # 设置cookies
    print('调用本地化cookie...')
    with open('./Lib/cookies.dll', 'r', encoding='utf-8') as f:
        cookies = eval(f.read())
        ID = cookies[2]['value']
    sess = requests.Session()
    for cookie in cookies:
        sess.cookies.set(name=cookie['name'], value=cookie['value'])
    print('调用本地化cookie完成...')

    # 等待并持续访问
    while tm().tm_hour == 21 and tm().tm_min <= 37:  # 21:37以前每两分钟刷新一次
        print('等待...    %02d:%02d:%02d' % (tm().tm_hour, tm().tm_min), tm().tm_sec)
        time.sleep(30)
        sess.get(url=f'http://seat.yangtzeu.edu.cn/libseat-ibeacon/nowActivity;jsessionid={ID}', headers=headers, stream=True, verify=False)
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
            res = sess.get(url=f'http://seat.yangtzeu.edu.cn/libseat-ibeacon/saveBook?seatId={seatId}&date={year}-{month}-{date_num}&start={start_num}&end={end_num}&type=1&captchaToken=', headers=headers, stream=True, verify=False)
        except:
            continue
        res.encoding = res.apparent_encoding
        with open('./Lib/res.txt', 'w+', encoding='utf-8') as f:
            f.write(res.text)
        res = json.loads(res.text)
        res = json.loads(res)
        status = res['status']
        if status == 'success':
            print('预约成功...')   
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
    date_num = choice_date()  # 获取预约日期，21点后运行默认为次日
    start_num, end_num = get_time(start_time=data_dict['start_time'], end_time=data_dict['end_time'])  # 计算预约时间Id
    if event == False:  # 未登录或登陆时间过长，则重新登陆
        try_login()
    else:  # 距上次登录不超过15分钟，则跳过登录操作
        print('近期已登录, 跳过登录...')
    res = get_seat(roomId=data_dict['roomId'], seatId=data_dict['seatId'], start_num=start_num, end_num=end_num, date_num=date_num)  # 尝试预约请求
    status = res['status']
    if status == 'success':  # 如果返回成功响应，则输出预约成功信息
        data = res['data']
        print_result(users, status=status, onDate=data['onDate'], begin=data['begin'], end=data['end'], location=data['location'])
    else:  # # 如果返回失败响应，则输出预约失败信息
        print_result(users, status=status, message=res['message'])


# 主程序入口
if __name__ == '__main__':
    print('开始运行...')
    # 获取当前时间戳
    now_time = int(time.time())
    # 读取上次登录时间戳
    try:
        with open('./Lib/login_time.dll', 'r', encoding='utf-8') as l_t:
            login_time = int(l_t.read())
    except FileNotFoundError as f_E:
        print('未找到登录时间戳文件，开始创建文件...')
        with open('./Lib/login_time.dll', 'w', encoding='utf-8') as n_t:
            n_t.write('1')
            print('登陆时间戳文件创建完成...')
            login_time = 0
    # 尝试预约操作
    try:
        # 登录间隔超过15分钟则重新登陆，否则跳过登录操作
        if (now_time - login_time) < 900:
            main(event=True)
        else:
            main(event=False)
    except Exception as E:
        print(E)
    while True:
        time.sleep(300)