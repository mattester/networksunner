# 华为 HCIE-Datacom 自动化脚本实战手册

目标：帮助你从零开始建立网络自动化能力。  
定位：不是为了炫 Python，而是让你把重复巡检、备份、校验、报表做成可复用工具。

---

## 1. 自动化学习顺序

建议按这个顺序学：

1. Python 基础
2. 文件操作
3. CSV / JSON
4. Paramiko 批量登录
5. 批量备份配置
6. 巡检脚本
7. 结果比对
8. NETCONF / RESTCONF
9. API 自动化

---

## 2. 环境准备

安装：

```bash
pip install paramiko
```

准备一个 `devices.csv`：

```csv
host,username,password
192.168.1.1,admin,Admin@123
192.168.1.2,admin,Admin@123
```

---

## 3. 脚本 1：批量登录并执行命令

```python
import csv
import paramiko

COMMAND = "display ip interface brief\n"

with open("devices.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        host = row["host"]
        username = row["username"]
        password = row["password"]
        print(f"== {host} ==")
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password, timeout=5)
            shell = ssh.invoke_shell()
            shell.send(COMMAND)
            output = shell.recv(65535).decode("utf-8", errors="ignore")
            print(output)
            ssh.close()
        except Exception as e:
            print(f"{host} failed: {e}")
```

### 作用

- 批量执行 display 命令
- 获取基本接口状态

### 你要学会什么

- CSV 读取
- Paramiko 登录
- 输出收集

---

## 4. 脚本 2：批量备份配置

```python
import csv
import os
import paramiko
from datetime import datetime

BACKUP_DIR = "backup_configs"
os.makedirs(BACKUP_DIR, exist_ok=True)

with open("devices.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        host = row["host"]
        username = row["username"]
        password = row["password"]
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password, timeout=5)
            shell = ssh.invoke_shell()
            shell.send("display current-configuration\n")
            output = shell.recv(200000).decode("utf-8", errors="ignore")
            filename = f"{host}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(os.path.join(BACKUP_DIR, filename), "w", encoding="utf-8") as fw:
                fw.write(output)
            ssh.close()
            print(f"{host} backup ok")
        except Exception as e:
            print(f"{host} backup failed: {e}")
```

### 工程价值

- 变更前基线备份
- 故障后对比配置
- 审计与回退准备

---

## 5. 脚本 3：巡检 OSPF 邻居

```python
import csv
import paramiko

def get_output(host, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password, timeout=5)
    shell = ssh.invoke_shell()
    shell.send(command + "\n")
    output = shell.recv(65535).decode("utf-8", errors="ignore")
    ssh.close()
    return output

with open("devices.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        output = get_output(row["host"], row["username"], row["password"], "display ospf peer")
        if "Full" in output:
            print(f"{row['host']} OSPF OK")
        else:
            print(f"{row['host']} OSPF CHECK")
```

### 价值

- 快速识别邻居异常
- 适合日常巡检

---

## 6. 脚本 4：巡检 BGP 邻居

```python
import csv
import paramiko

def check_bgp(output):
    if "Established" in output:
        return "OK"
    return "CHECK"

with open("devices.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        host = row["host"]
        username = row["username"]
        password = row["password"]
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password, timeout=5)
            shell = ssh.invoke_shell()
            shell.send("display bgp peer\n")
            output = shell.recv(65535).decode("utf-8", errors="ignore")
            print(host, check_bgp(output))
            ssh.close()
        except Exception as e:
            print(host, "FAILED", e)
```

---

## 7. 脚本 5：生成巡检报告

```python
import csv

rows = [
    {"host": "192.168.1.1", "ospf": "OK", "bgp": "OK"},
    {"host": "192.168.1.2", "ospf": "CHECK", "bgp": "OK"},
]

with open("report.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["host", "ospf", "bgp"])
    writer.writeheader()
    writer.writerows(rows)
```

### 价值

- 从“能执行命令”走向“可交付结果”

---

## 8. 自动化训练思路

### 8.1 从小脚本开始

先写：

- 读取文件
- 输出设备清单
- 登录一台设备
- 登录多台设备
- 执行一条命令
- 执行多条命令

### 8.2 再做工程化

逐步加入：

- 错误处理
- 日志
- 超时重试
- 报表输出
- 配置差异比对

---

## 9. 高级技巧

### 技巧 1：把脚本和排障结合

例如：

- 批量查 OSPF 邻居
- 批量查 BGP 邻居
- 批量查接口 down
- 批量查 CPU 高

### 技巧 2：先做只读，再做写入

顺序一定是：

1. 先做 show/display 自动化
2. 再做备份自动化
3. 最后再做配置下发自动化

### 技巧 3：输出可读结果

脚本不是给自己炫的，是给运维、团队、主管看的。  
所以输出最好有：

- 报告
- CSV
- Markdown
- 清晰的异常标记

---

## 10. 自动化面试怎么讲

你可以这样说：

- 我不是单纯学 Python，而是围绕网络运维场景做自动化
- 我做过配置备份、邻居巡检、接口巡检、异常报表
- 自动化的价值在于降低重复人工操作风险，提高巡检效率

---

## 11. 下一步学习建议

当你掌握 Paramiko 之后，可以继续往这些方向进：

- NAPALM / Netmiko
- NETCONF / ncclient
- RESTCONF / requests
- YANG 模型
- Telemetry 数据采集
- Ansible for Network

---

## 12. 结语

自动化不是额外技能，而是高级网络专家的必备能力。  
真正拉开差距的是：

- 你能不能把重复工作抽象出来
- 你能不能把经验写成脚本
- 你能不能让网络运维更稳定、更可控

