import hashlib
import time
from urllib.parse import quote
from baidupcs_py.baidupcs import BaiduPCSApi
from baidupcs_py.baidupcs.inner import (CloudTask, FromTo, PcsAuth, PcsFile,
                                        PcsMagnetFile, PcsQuota, PcsSharedLink,
                                        PcsSharedPath, PcsUser, PcsUserProduct)
from baidupcs_py.commands.display import display_files, display_from_to
from bd_unlocksbox import BaiduSafeBox
headers = {
    'User-Agent': 'netdisk;11.6.3;',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
}



# 隐藏空间list
def list_sbox(remotepath: str,
              desc: str = 'desc',
              name: bool = False,
              time: bool = False,
              size: bool = False,
              ):
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



# 文件列表展示
def get_list():
    remotepath = '/_pcs_.safebox/'
    info = list_sbox(remotepath, time=True)
    if info['errno'] == 0:
        print(info)
        pcs_files = [PcsFile.from_(v) for v in info.get("list", [])]
        display_files(pcs_files, remotepath)
    elif info['errno'] == -9:
        print('目录不存在')
    elif info['errno'] == 27:
        print('缺少SBOXTKN值或SBOXTKN过期')
    else:
        print(info)



# 移动文件操作  返回taskid
# 返回结果
#{'errno': 0, 'info': [], 'request_id': 1228540435613264910, 'taskid': 648701096876893}
def _move(*remotepaths: str):
    params = (
        ('opera', 'move'),
        ('async', '2'),
        ('onnest', 'fail'),
        ('channel', 'chunlei'),
        ('web', '1'),
        ('app_id', '250528'),
        ('bdstoken', bdstoken),
        ('clienttype', '0'),
    )
    sources, dest = remotepaths[:-1], remotepaths[-1]
    print(sources, dest)
    filelist = []
    for s in sources:
        dict_file = {}
        dict_file['path'] = s
        dict_file['dest'] = dest
        dict_file['newname'] = s.split('/')[-1]
        filelist.append(dict_file)
    print(filelist)
    filelist = str(filelist).replace('\'', '\"')
    data = f'filelist={quote(filelist)}'
    print(data)
    resp = api._baidupcs._session.post(
        'https://pan.baidu.com/api/filemanager', headers=headers, params=params, data=data)
    res = resp.json()
    print(res)
    return filelist, res['taskid']


# 查询taskid任务完成结果
# 返回结果
#{'errno': 0, 'request_id': 1228541945609870939, 'task_errno': 0, 'status': 'success', 'list': [{'from': '/6-3-901.dump', 'to': '/_pcs_.safebox/6-3-901.dump'}], 'total': 1}
def get_taskquery(filelist, taskid):
    params = (
        ('taskid', str(taskid)),
        ('channel', 'chunlei'),
        ('web', '1'),
        ('app_id', '250528'),
        ('bdstoken', bdstoken),
        ('clienttype', '0'),
    )
    data = f'filelist={quote(filelist)}'
    resp = api._baidupcs._session.post(
        'https://pan.baidu.com/share/taskquery', headers=headers, params=params, data=data)
    print(resp.json())



# 移进移出隐藏空间
def move():
    #remotepaths = ['/2021春节上映/6-3-901.dump', '/_pcs_.safebox']
    remotepaths = ['/_pcs_.safebox/6-3-901.dump', '/']
    filelist, taskid = _move(*remotepaths)
    time.sleep(5)
    get_taskquery(filelist, taskid)


cookies = {
    'BDUSS': '',
    'STOKEN': '',
}
pwd = ''
bdstoken = hashlib.md5(cookies['BDUSS'].encode()).hexdigest().lower()
api = BaiduPCSApi(cookies=cookies)
print(api.cookies)

bd = BaiduSafeBox(cookies, pwd)
sboxtkn = bd.unlockbox()
print(sboxtkn)
if sboxtkn is None:
    print('获取SBOXTKN失败')
else:
    api._baidupcs._cookies_update({'SBOXTKN': sboxtkn})
    print(api.cookies)
    # get_list()  #获取隐藏空间目录
    move()  #移动文件