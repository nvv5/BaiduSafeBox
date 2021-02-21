# BaiduSafeBox  
基于[BaiduPCS-Py](https://github.com/PeterDing/BaiduPCS-Py)的api接口开发的百度网盘隐藏空间demo。
## 安装
- 需要 Python 版本大于或等于 3.7  
- 需要安装BaiduPCS-Py  
```
pip3 install BaiduPCS-Py
```
## 文件介绍
### bd_unlocksbox.py
用于实现隐藏空间的解锁，返回一个隐藏空间所需的`SBOXTKN`的cookie。  
示例  
```
cookies = {
    'BDUSS': '',
    'STOKEN': '',
    }
pwd=''  #二级密码
bd = BaiduSafeBox(cookies,pwd)
sboxtkn=bd.unlockbox()
print(sboxtkn)
```
### pcs_api.py
利用BaiduPCS-Py的api所展示的一个demo。  

