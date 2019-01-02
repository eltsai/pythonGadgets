#  A Relay DNS中继服务器

### Environment

linux，python3.

### Run Server

under `/src`

```bash
sudo python3 main.py
```
to start this dns server (running at 127.0.0.1)
### Debug Mode
use
```bash
sudo python3 dnsrelay [-d][-dd] [public-server] [local-cache]
```
to enter debug mode
### Tests
use
```bash
dig your-domain @127.0.0.1
```
or
```bash
sudo chmod +x dig.sh && ./dig.sh
```
to test this server

### 实现功能

- [x] 不良网站拦截功能：在本地ip cache中找到对应ip为'0.0.0.0'，返回域名不存在

- [x] 服务器功能&中继功能：

- [x] 调试级别1：`sudo python3 dnsrelay`

- [x] 调试级别2: `sudo python3 dnsrelay -d [public-server] [local-cache]`

- [x] 调试级别3：`sudo python3 -dd [public-server]`

- [x] 多客户端并发&超时处理：




