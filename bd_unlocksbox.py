import requests
import hashlib
from skimage import io


class BaiduSafeBox():
    def __init__(self, cookies, pwd):
        self.cookies = cookies
        self.pwd = pwd
        if cookies and cookies.get("BDUSS", ""):
            self.bduss = cookies["BDUSS"]
        if cookies and cookies.get("STOKEN", ""):
            self.stoken = cookies["STOKEN"]
        self.bdstoken = hashlib.md5(self.bduss.encode()).hexdigest().lower()
        self.headers = {
            'User-Agent': 'netdisk;11.6.3;',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }

    def unlockbox(self):
        data = {
            'passwd': self.pwd,
            'type': '0',  # 1是我的卡包  0是隐藏空间
            'bdstoken': self.bdstoken
        }
        response = self.login_safebox(data)
        res = response.json()
        if res['errno'] == -20:
            yzm, vcode_str = self.getcaptcha()
            data['vcode_input'] = yzm
            data['vcode_str'] = vcode_str
            response = self.login_safebox(data)
            res = response.json()
            if res['errno'] == 0:
                print('登录成功')
                sboxtkn = response.cookies['SBOXTKN']
            elif res['errno'] == 26:
                print('二级密码错误')
            else:
                print(res)
                sboxtkn = None
        elif res['errno'] == 0:
            print('登录成功')
            sboxtkn = response.cookies['SBOXTKN']
        elif res['errno'] == 26:
            print('二级密码错误')
        else:
            print(res)
            sboxtkn = None
        return sboxtkn

    def login_safebox(self,  data):
        response = requests.post('https://pan.baidu.com/sbox/auth/unlockbox',
                                 headers=self.headers, cookies=self.cookies, data=data)
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
    # cookies = {'BDUSS': '','STOKEN': '',}
    cookies = {'BDUSS': ''}
    pwd = ''  # 二级密码
    bd = BaiduSafeBox(cookies, pwd)
    sboxtkn = bd.unlockbox()
    print(sboxtkn)
