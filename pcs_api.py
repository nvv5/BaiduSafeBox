from baidupcs_py.baidupcs import BaiduPCSApi
from bd_unlocksbox import BaiduSafeBox
from baidupcs_py.commands.display import display_files
from baidupcs_py.baidupcs.inner import (
    PcsFile,
    PcsMagnetFile,
    PcsSharedLink,
    PcsSharedPath,
    FromTo,
    PcsAuth,
    PcsUserProduct,
    PcsUser,
    PcsQuota,
    CloudTask,
)


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
    _bdstoken = api.bdstoken()
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

#填写bduss和stoken
cookies = {
    'BDUSS': '',
    'STOKEN': '',
}
pwd = ''  # 二级密码

api = BaiduPCSApi(cookies=cookies)
bd = BaiduSafeBox(cookies, pwd)
sboxtkn = bd.unlockbox()
# print(sboxtkn)
api._baidupcs._cookies_update({'SBOXTKN': sboxtkn})
# print(api.cookies)
remotepath = '/_pcs_.safebox/'
info = list_sbox(remotepath, time=True)
# print(info)
pcs_files = [PcsFile.from_(v) for v in info.get("list", [])]
# pcs接口没有权限访问隐藏空间
# print(api.list(remotepath='/_pcs_.safebox'))

display_files(pcs_files, remotepath)
