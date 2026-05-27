# 华为 HCIE-Datacom 实验命令参考

用途：配合 `华为HCIE_Datacom_学习手册.md` 与 `60天打卡表.csv` 使用  
适用范围：华为 VRP 风格设备命令参考  
重要说明：

- 不同产品线、VRP 版本、交换机/路由器系列之间命令会有细微差异
- 本文偏向 Datacom 常见 VRP 语法
- 高阶园区、CloudCampus、SRv6、NCE 自动化等部分，真实项目和考试环境应以当期官方文档和实验平台为准

---

## 1. 通用操作

### 1.1 进入系统视图

```text
<HUAWEI> system-view
[HUAWEI]
```

### 1.2 修改设备名

```text
[HUAWEI] sysname AR1
```

### 1.3 查看当前配置

```text
<HUAWEI> display current-configuration
<HUAWEI> display current-configuration interface GigabitEthernet 0/0/1
```

### 1.4 保存配置

```text
<HUAWEI> save
```

### 1.5 查看接口摘要

```text
<HUAWEI> display ip interface brief
<HUAWEI> display interface brief
```

---

## 2. 基础 IP 与接口

### 2.1 配置三层接口 IP

```text
[AR1] interface GigabitEthernet 0/0/0
[AR1-GigabitEthernet0/0/0] ip address 192.168.1.1 24
```

### 2.2 配置 Loopback

```text
[AR1] interface LoopBack 0
[AR1-LoopBack0] ip address 1.1.1.1 32
```

### 2.3 关闭/开启接口

```text
[AR1-GigabitEthernet0/0/0] shutdown
[AR1-GigabitEthernet0/0/0] undo shutdown
```

### 2.4 验证

```text
<AR1> display ip interface brief
<AR1> display interface GigabitEthernet 0/0/0
<AR1> ping 192.168.1.2
```

排障入口：

- 接口是否 up/up
- IP 地址是否同网段
- 对端接口是否打开

---

## 3. VLAN / Access / Trunk / Vlanif

根据华为官方 VLAN 文档，`port link-type trunk`、`port trunk allow-pass vlan ...`、`port default vlan ...` 为核心配置命令。citeturn0search1turn0search3

### 3.1 创建 VLAN

```text
[SW1] vlan batch 10 20 30
```

### 3.2 Access 接口加入 VLAN

```text
[SW1] interface GigabitEthernet 0/0/1
[SW1-GigabitEthernet0/0/1] port link-type access
[SW1-GigabitEthernet0/0/1] port default vlan 10
```

### 3.3 Trunk 接口放行 VLAN

```text
[SW1] interface GigabitEthernet 0/0/24
[SW1-GigabitEthernet0/0/24] port link-type trunk
[SW1-GigabitEthernet0/0/24] port trunk allow-pass vlan 10 20 30
[SW1-GigabitEthernet0/0/24] port trunk pvid vlan 10
```

### 3.4 配置 VLANIF 网关

```text
[SW1] interface Vlanif 10
[SW1-Vlanif10] ip address 192.168.10.254 24
[SW1] interface Vlanif 20
[SW1-Vlanif20] ip address 192.168.20.254 24
```

### 3.5 验证

```text
<SW1> display vlan
<SW1> display port vlan
<SW1> display ip interface brief
<SW1> display mac-address
```

排障顺序：

1. VLAN 是否创建
2. 接口链路类型对不对
3. trunk 是否放行了目标 VLAN
4. Vlanif 是否有 IP 且 up
5. PC 网关是否正确

---

## 4. STP / MSTP

### 4.1 启用 STP

```text
[SW1] stp enable
```

### 4.2 配置根桥优先级

```text
[SW1] stp priority 4096
[SW2] stp priority 8192
```

### 4.3 配置 MSTP 区域

```text
[SW1] stp mode mstp
[SW1] stp region-configuration
[SW1-mst-region] region-name campus
[SW1-mst-region] revision-level 1
[SW1-mst-region] instance 1 vlan 10 20
[SW1-mst-region] active region-configuration
```

### 4.4 验证

```text
<SW1> display stp brief
<SW1> display stp
<SW1> display stp interface GigabitEthernet 0/0/24
```

重点观察：

- 根桥是谁
- 根端口是谁
- 是否有阻塞口

---

## 5. Eth-Trunk 链路聚合

### 5.1 创建聚合组

```text
[SW1] interface Eth-Trunk 1
[SW1-Eth-Trunk1] mode lacp-static
```

### 5.2 成员接口加入聚合组

```text
[SW1] interface GigabitEthernet 0/0/23
[SW1-GigabitEthernet0/0/23] eth-trunk 1
[SW1] interface GigabitEthernet 0/0/24
[SW1-GigabitEthernet0/0/24] eth-trunk 1
```

### 5.3 聚合口配置 Trunk

```text
[SW1] interface Eth-Trunk 1
[SW1-Eth-Trunk1] port link-type trunk
[SW1-Eth-Trunk1] port trunk allow-pass vlan 10 20 30
```

### 5.4 验证

```text
<SW1> display eth-trunk 1
<SW1> display lacp statistics eth-trunk 1
```

---

## 6. 静态路由与缺省路由

### 6.1 配置静态路由

```text
[AR1] ip route-static 10.2.2.0 24 192.168.12.2
```

### 6.2 配置缺省路由

```text
[AR1] ip route-static 0.0.0.0 0 192.168.12.2
```

### 6.3 浮动静态

```text
[AR1] ip route-static 0.0.0.0 0 192.168.12.2 preference 60
[AR1] ip route-static 0.0.0.0 0 192.168.13.2 preference 100
```

### 6.4 验证

```text
<AR1> display ip routing-table
<AR1> display ip routing-table protocol static
<AR1> tracert 10.2.2.2
```

---

## 7. OSPF

### 7.1 启动 OSPF 进程

```text
[AR1] ospf 1 router-id 1.1.1.1
```

### 7.2 宣告网段

```text
[AR1-ospf-1] area 0
[AR1-ospf-1-area-0.0.0.0] network 192.168.12.0 0.0.0.255
[AR1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0
```

### 7.3 配置认证（示例）

```text
[AR1] interface GigabitEthernet 0/0/0
[AR1-GigabitEthernet0/0/0] ospf authentication-mode simple plain huawei
```

### 7.4 传播缺省路由

```text
[AR1-ospf-1] default-route-advertise
```

### 7.5 路由引入

```text
[AR1-ospf-1] import-route static
```

### 7.6 验证

```text
<AR1> display ospf peer
<AR1> display ospf interface
<AR1> display ospf routing
<AR1> display ip routing-table protocol ospf
```

排障重点：

- `display ospf peer`
- `display ip interface brief`
- 区域、认证、Hello/Dead、MTU、网络类型

---

## 8. ACL

### 8.1 基本 ACL

```text
[AR1] acl 2000
[AR1-acl-basic-2000] rule 5 permit source 192.168.10.0 0.0.0.255
[AR1-acl-basic-2000] rule 10 deny
```

### 8.2 高级 ACL

```text
[AR1] acl 3000
[AR1-acl-adv-3000] rule 5 permit tcp source 192.168.10.0 0.0.0.255 destination 10.1.1.0 0.0.0.255 destination-port eq 80
[AR1-acl-adv-3000] rule 10 deny ip
```

### 8.3 接口调用 ACL

```text
[AR1] interface GigabitEthernet 0/0/0
[AR1-GigabitEthernet0/0/0] traffic-filter inbound acl 3000
```

### 8.4 验证

```text
<AR1> display acl 3000
<AR1> display current-configuration interface GigabitEthernet 0/0/0
```

---

## 9. NAT

### 9.1 Easy-IP

```text
[AR1] acl 2001
[AR1-acl-basic-2001] rule 5 permit source 192.168.10.0 0.0.0.255

[AR1] interface GigabitEthernet 0/0/1
[AR1-GigabitEthernet0/0/1] nat outbound 2001
```

### 9.2 NAPT 地址池（部分平台）

```text
[AR1] nat address-group 1 100.1.1.10 100.1.1.20
[AR1] acl 2001
[AR1-acl-basic-2001] rule 5 permit source 192.168.10.0 0.0.0.255
[AR1] interface GigabitEthernet 0/0/1
[AR1-GigabitEthernet0/0/1] nat outbound 2001 address-group 1
```

### 9.3 验证

```text
<AR1> display nat session all
<AR1> display nat outbound
```

---

## 10. DHCP

### 10.1 全局开启 DHCP

```text
[AR1] dhcp enable
```

### 10.2 接口地址池发放

```text
[AR1] interface Vlanif 10
[AR1-Vlanif10] ip address 192.168.10.254 24
[AR1-Vlanif10] dhcp select interface
```

### 10.3 全局地址池

```text
[AR1] ip pool VLAN20
[AR1-ip-pool-VLAN20] network 192.168.20.0 mask 255.255.255.0
[AR1-ip-pool-VLAN20] gateway-list 192.168.20.254
[AR1-ip-pool-VLAN20] dns-list 114.114.114.114
```

### 10.4 验证

```text
<AR1> display ip pool
<AR1> display dhcp server ip-in-use
```

---

## 11. IPv6 基础

### 11.1 开启 IPv6

```text
[AR1] ipv6
```

### 11.2 接口配置 IPv6

```text
[AR1] interface GigabitEthernet 0/0/0
[AR1-GigabitEthernet0/0/0] ipv6 enable
[AR1-GigabitEthernet0/0/0] ipv6 address 2001:db8:12::1/64
```

### 11.3 静态 IPv6 路由

```text
[AR1] ipv6 route-static 2001:db8:2::/64 2001:db8:12::2
```

### 11.4 验证

```text
<AR1> display ipv6 interface brief
<AR1> display ipv6 routing-table
<AR1> ping ipv6 2001:db8:12::2
```

---

## 12. BGP

华为官方 `display bgp peer` 与 `display bgp routing-table` 是 BGP 验证核心命令。citeturn0search2turn0search0

### 12.1 建立 BGP 进程

```text
[AR1] bgp 65001
[AR1-bgp] router-id 1.1.1.1
```

### 12.2 配置 EBGP 邻居

```text
[AR1-bgp] peer 192.168.12.2 as-number 65002
```

### 12.3 宣告本地网段

```text
[AR1-bgp] network 10.1.1.0 255.255.255.0
```

### 12.4 配置 IBGP 邻居

```text
[AR1-bgp] peer 2.2.2.2 as-number 65001
[AR1-bgp] peer 2.2.2.2 connect-interface LoopBack 0
```

### 12.5 Next-Hop-Self

```text
[AR1-bgp] peer 2.2.2.2 next-hop-local
```

### 12.6 Local Preference（route-policy）

```text
[AR1] route-policy LP permit node 10
[AR1-route-policy] apply local-preference 200

[AR1] bgp 65001
[AR1-bgp] peer 192.168.12.2 route-policy LP import
```

### 12.7 AS-Path Prepend（route-policy）

```text
[AR1] route-policy PREPEND permit node 10
[AR1-route-policy] apply as-path 65001 65001 65001 additive

[AR1] bgp 65001
[AR1-bgp] peer 192.168.13.2 route-policy PREPEND export
```

### 12.8 验证

```text
<AR1> display bgp peer
<AR1> display bgp routing-table
<AR1> display bgp routing-table 10.1.1.0
<AR1> display ip routing-table protocol bgp
```

排障重点：

- 邻居是否 Established
- router-id 是否冲突
- AS 是否正确
- Loopback 建邻是否有可达路由
- next-hop 是否可达
- route-policy 是否误过滤

---

## 13. MPLS / LDP

### 13.1 开启 MPLS

```text
[P] mpls lsr-id 1.1.1.1
[P] mpls
```

### 13.2 接口开启 MPLS / LDP

```text
[P] interface GigabitEthernet 0/0/0
[P-GigabitEthernet0/0/0] mpls
[P-GigabitEthernet0/0/0] mpls ldp
```

### 13.3 启动 LDP

```text
[P] mpls ldp
```

### 13.4 验证

```text
<P> display mpls ldp session
<P> display mpls lsp
<P> display mpls forwarding-table
```

---

## 14. MPLS L3VPN

### 14.1 创建 VPN 实例

```text
[PE1] ip vpn-instance VPN-A
[PE1-vpn-instance-VPN-A] ipv4-family
[PE1-vpn-instance-VPN-A-af-ipv4] route-distinguisher 100:1
[PE1-vpn-instance-VPN-A-af-ipv4] vpn-target 100:1 both
```

### 14.2 接口绑定 VRF

```text
[PE1] interface GigabitEthernet 0/0/2
[PE1-GigabitEthernet0/0/2] ip binding vpn-instance VPN-A
[PE1-GigabitEthernet0/0/2] ip address 10.10.10.1 24
```

### 14.3 建立 MP-BGP VPNv4 邻居

```text
[PE1] bgp 65000
[PE1-bgp] peer 2.2.2.2 as-number 65000
[PE1-bgp] peer 2.2.2.2 connect-interface LoopBack 0
[PE1-bgp] ipv4-family vpnv4
[PE1-bgp-af-vpnv4] peer 2.2.2.2 enable
```

### 14.4 CE 路由引入 VRF（示例）

```text
[PE1] bgp 65000
[PE1-bgp] ipv4-family vpn-instance VPN-A
[PE1-bgp-VPN-A] import-route direct
```

### 14.5 验证

```text
<PE1> display ip vpn-instance
<PE1> display bgp vpnv4 all peer
<PE1> display bgp vpnv4 all routing-table
<PE1> display ip routing-table vpn-instance VPN-A
<PE1> display mpls forwarding-table
```

排障顺序：

1. IGP
2. LDP
3. MP-BGP VPNv4
4. VRF/RD/RT
5. VPN 路由是否进表
6. 标签转发是否存在

---

## 15. 常用 display 命令总表

| 场景 | 核心命令 |
|---|---|
| 接口状态 | `display ip interface brief` |
| 二层接口与 VLAN | `display vlan` `display port vlan` |
| MAC 学习 | `display mac-address` |
| STP | `display stp brief` |
| 聚合 | `display eth-trunk` |
| 路由表 | `display ip routing-table` |
| OSPF 邻居 | `display ospf peer` |
| OSPF 路由 | `display ospf routing` |
| ACL | `display acl all` |
| NAT | `display nat session all` |
| DHCP | `display ip pool` |
| BGP 邻居 | `display bgp peer` |
| BGP 路由 | `display bgp routing-table` |
| MPLS LDP | `display mpls ldp session` |
| MPLS 转发表 | `display mpls forwarding-table` |
| VPN 路由 | `display ip routing-table vpn-instance <name>` |

---

## 16. 最重要的排障习惯

### 16.1 每次实验都按这个顺序查

1. `display interface brief`
2. `display ip interface brief`
3. `display current-configuration interface ...`
4. `display ip routing-table`
5. 对应协议 `display` 命令

### 16.2 每次改配置前做三件事

```text
display current-configuration
display ip routing-table
save
```

### 16.3 每次实验后做四件事

- 保存配置
- 导出拓扑图
- 记录故障点
- 写 5 行复盘

---

## 17. 高阶模块提醒

下列模块在不同实验环境中差异更大，建议以你后续确定的具体平台为准：

- VXLAN / BGP EVPN
- CloudCampus / NAC / iMaster NCE
- SD-WAN / CloudWAN
- Segment Routing / SRv6
- NETCONF / RESTCONF / Telemetry

建议做法：

1. 先学原理与控制面逻辑
2. 再确定实验平台
3. 再按平台版本找对应命令

---

## 18. 官方参考链接

以下内容用于校准通用命令和验证命令：

- 华为 VLAN 配置命令文档：https://support.huawei.com/enterprise/en/doc/EDOC1100514211/834147df/vlan-configuration-commands
- 华为 VLAN 基础说明：https://support.huawei.com/enterprise/en/doc/EDOC1100086556
- 华为 `display bgp peer` 文档：https://info.support.huawei.com/hedex/api/pages/EDOC1100149308/AEJ0713J/18/resources/cli_vrp/display_bgp_peer.html
- 华为 `display bgp routing-table` 文档：https://support.huawei.com/enterprise/en/doc/EDOC1100333812/bdd63b27/display-bgp-routing-table

说明：

- 本手册中的命令示例为学习参考
- 实际考试或项目环境，请以对应 VRP 版本与设备官方命令参考为准

