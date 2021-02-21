import requests
import hashlib
from skimage import io


class BaiduSafeBox():
    def __init__(self,cookies,pwd):
        self.cookies = cookies
        self.pwd=pwd
        if cookies and cookies.get("BDUSS", ""):
            self.bduss = cookies["BDUSS"]
        if cookies and cookies.get("STOKEN", ""):
            self.stoken = cookies["STOKEN"]
        self.bdstoken = hashlib.md5(self.bduss.encode()).hexdigest().lower()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://pan.baidu.com/disk/home?_at_=1613750417379',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    def unlockbox(self):
        params = (
            ('channel', 'chunlei'),
            ('web', '1'),
            ('app_id', '250528'),
            ('bdstoken', self.bdstoken),
        )

        data = {
            'passwd': self.pwd,
            'type': '0',  # 1是我的卡包  0是隐藏空间
            'bdstoken': self.bdstoken
        }
        response = self.login_safebox(params, data)
        res = response.json()
        if res['errno'] == -20:
            yzm, vcode_str = self.getcaptcha()
            data['vcode_input'] = yzm
            data['vcode_str'] = vcode_str
            response = self.login_safebox(params, data)
            res = response.json()
            if res['errno'] == 0:
                print('登录成功')
                sboxtkn=response.cookies['SBOXTKN']
            else:
                print(res)
                sboxtkn=None
        elif res['errno'] == 0:
            print('登录成功')
            sboxtkn=response.cookies['SBOXTKN']
        else:
            print(res)
            sboxtkn=None
        return sboxtkn

    def login_safebox(self, params, data):
        response = requests.post('https://pan.baidu.com/sbox/auth/unlockbox',
                                 headers=self.headers, params=params, cookies=self.cookies, data=data)
        return response

    def getcaptcha(self):
        params = (
            ('prod', 'sbox'),
            ('channel', 'chunlei'),
            ('web', '1'),
            ('app_id', '250528'),
            ('bdstoken', self.bdstoken),
        )
        response = requests.get('https://pan.baidu.com/api/getcaptcha',
                                headers=self.headers, params=params, cookies=self.cookies)
        res = response.json()
        print(res)
        img_url = res['vcode_img']
        vcode_str = res['vcode_str']
        raw_ans = res['raw_ans']
        print('参考答案字符：', raw_ans)
        self.show_img(img_url)
        yzm = input('输入验证码：')
        return yzm, vcode_str

    def show_img(self, img_url):
        # img_url='https://pan.baidu.com/genimage?33324238656332346361663334656637323237633636373637643239666664336662343234393631343535303030303030303030303030303031363133373531353337E36349CB7498F246F991AA6D7BAD06A5'
        image = io.imread(img_url)
        io.imshow(image)
        io.show()


if __name__ == '__main__':
    cookies = {
    'BDUSS': '',
    'STOKEN': '',
    }
    pwd=''  #二级密码
    bd = BaiduSafeBox(cookies,pwd)
    sboxtkn=bd.unlockbox()
    print(sboxtkn)
