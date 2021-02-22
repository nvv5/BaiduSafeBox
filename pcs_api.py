import hashlib
from baidupcs_py.baidupcs import BaiduPCSApi
from baidupcs_py.baidupcs.inner import (CloudTask, FromTo, PcsAuth, PcsFile,
                                        PcsMagnetFile, PcsQuota, PcsSharedLink,
                                        PcsSharedPath, PcsUser, PcsUserProduct)
from baidupcs_py.commands.display import display_files
from bd_unlocksbox import BaiduSafeBox


def list_sbox(remotepath: str,
              desc: str = 'desc',
              name: bool = False,
              time: bool = False,
              size: bool = False,
              ):
    headers = {
        'User-Agent': 'netdisk;11.6.3;YAL-AL00;android-android;10;JSbridge4.4.0;jointBridge;1.1.0;',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }
    _bdstoken = bdstoken
    url = 'https://pan.baidu.com/api/list'
    if desc == 'desc':
        desc_order = '1'
    else:
        desc_order = '0'
    # desc_dict={'asc':'0','desc':'1'}
    orderby = None
    if name:
        orderby = "name"
    elif time:
        orderby = "time"
    elif size:
        orderby = "size"
    else:
        orderby = "name"
    params = {
        'dir': str(remotepath),
        'start': '0',
        'limit': '50',
        'order': orderby,
        # 'desc':'0',  #升序排列
        # 'desc': '1',  # 降序排列
        'desc': desc_order,
        'preset': '1',
        'bdstoken': _bdstoken
    }
    resp = api._baidupcs._request_get(url, params=params, headers=headers)
    return resp.json()


cookies = {'BDUSS': ''}
pwd = ''
bdstoken = hashlib.md5(cookies['BDUSS'].encode()).hexdigest().lower()
api = BaiduPCSApi(cookies=cookies)
bd = BaiduSafeBox(cookies, pwd)
sboxtkn = bd.unlockbox()
print(sboxtkn)
if sboxtkn is None:
    print('获取SBOXTKN失败')
else:
    api._baidupcs._cookies_update({'SBOXTKN': sboxtkn})
    print(api.cookies)
    remotepath = '/_pcs_.safebox/'
    info = list_sbox(remotepath, time=True)

    if info['errno'] == 0:
        print(info)
        pcs_files = [PcsFile.from_(v) for v in info.get("list", [])]
        display_files(pcs_files, remotepath)
    if info['errno'] == -9:
        print('目录不存在')
    elif info['errno'] == 27:
        print('缺少SBOXTKN值或SBOXTKN过期')
    else:
        print(info)
# pcs接口没有权限访问隐藏空间
# print(api.list(remotepath='/_pcs_.safebox'))
