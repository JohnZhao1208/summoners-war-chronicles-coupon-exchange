import json
import re
import requests
import sys
import urllib.request

SERVER_BASE_FDH = '771|SEA|6|全球服务器亚洲地区 - 费得海'
SERVER_BASE_LFNS = '771|SEA|7|全球服务器亚洲地区 - 露菲纳斯'
SERVER_BASE_ALE = '771|SEA|5|全球服务器亚洲地区 - 阿里尔'

if __name__ == '__main__':
    print('请选择服务器: 1=阿里尔,2=费得海,3=露菲纳斯')
    server = input("请选择服务器: ")
    cs_code = input("输入cs_code: ")



    try:
        open('coupons.txt', 'r')
        with open('coupons.txt', 'r') as f:
            lines = f.readlines()
            coupons = [line.strip() for line in lines]
    except FileNotFoundError:
        print('coupons.txt文件不存在,从远程读取!')
        url = 'https://gitee.com/nsbcgwdgcshstz/summoners-war-chronicles-coupon-exchange/raw/master/coupons.txt'
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8') # 将字节流解码为字符串
        coupons = data.split('\r\n') # 将字符串按行分割为数组

    if server == '2':
        serverFullName = SERVER_BASE_FDH
    elif server == '3':
        serverFullName = SERVER_BASE_LFNS
    elif server == '1':
        serverFullName = SERVER_BASE_ALE
    else:
        print('服务器选择错误!!!')
        sys.exit(1)

    headers = {
        'accept-language': 'zh-CN,zh;q=0.9'
    }
    response = requests.get('https://coupon.withhive.com/771', headers=headers)
    pattern = r"'Page-Key': '(.+)'"
    matches = re.findall(pattern, response.text)
    pageKey = matches[0] if matches else ''

    if not pageKey:
        print('pageKey获取失败!!!')
        sys.exit(1)

    print(f'初始化PageKey={pageKey}')

    for coupon in coupons:
        data = {
            "language": "zh-hans",
            "server": serverFullName,
            "cs_code": cs_code,
            "coupon": coupon,
            "additional_info": pageKey
        }
        headers = {
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'page-key': pageKey
        }

        response = requests.post('https://coupon.withhive.com/tp/coupon/use',
                                 headers=headers, data=json.dumps(data))
        result = response.json()
        print(f"{cs_code}-{server}-{coupon}-{result['msg']}")

    input(f'兑换结束!!!')
