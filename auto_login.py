import socket
import requests
import yaml


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
def login(ip:str, student_id:str, device:str, password:str, ISP:str) -> str:
    # 考虑校园网情况
    if ISP != '':
        ISP = '%40' + ISP
    url = f'http://210.29.79.141:801/eportal/?' \
          f'c=Portal&' \
          f'a=login&' \
          f'callback=dr1003&' \
          f'login_method=1&' \
          f'user_account=%2C{device}%2C{student_id}{ISP}&user_password={password}&' \
          f'wlan_user_ip={ip}&' \
          f'wlan_user_ipv6=&' \
          f'wlan_user_mac=000000000000&' \
          f'wlan_ac_ip=&' \
          f'wlan_ac_name=&' \
          f'jsVersion=3.3.2&' \
          f'v=7656'
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    return res.text

if __name__ == '__main__':
    ip = get_host_ip()
   

    with open('./infomation.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    
     # 学号
    student_id = result['student_id']
    # 运营商
    ISP = result['ISP']
    # 密码
    password = result['password']
    # 设备 PC端为0 移动端为1
    device = result['device']

    ret =  login(ip=ip, student_id=student_id, device=device,password=password, ISP=ISP)
    
    if '"result":"1"' in ret:
        print('登录成功')
    else:
        print('登录失败')

    