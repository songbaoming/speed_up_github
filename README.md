# GitHub 访问加速

## 使用方法

**确保安装了 Python3**！在管理员权限下，使用 Python3 执行 update_hosts_github_ip.py。

- Windows，使用管理员权限打开 cmd，执行 `python update_hosts_github_ip.py`；

- Linux/macOS，打开终端，执行 `sudo python3 update_hosts_github_ip.py`。

**尽量使用 SSH 协议访问！**

## 其他问题解决思路

- 如果执行该脚本之后，GitHub 界面显示有问题，使用浏览器的开发者工具（Chrome/Firefox 按 F12），从控制台看有哪些资源加载失败了，然后把资源对应的域名加入到脚本的 `DOMAIN_NAME` 列表里，重新执行脚本。
