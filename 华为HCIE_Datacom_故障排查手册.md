# 华为 HCIE-Datacom 故障排查手册

目标：把常见网络故障按“现象 - 可能原因 - 验证命令 - 修复动作”拆开，帮助你形成高级网络工程师的排障思维。  
适用范围：华为 VRP 风格网络设备、Datacom 常见实验与项目场景。  
核心原则：先确认范围，再确认分层，再确认变更，最后再确认控制面与数据面。

---

## 1. 排障总原则

### 1.1 不要上来就改配置

先做四件事：

1. 记录故障现象
2. 确认影响范围
3. 确认最近变更
4. 收集当前状态

建议先执行：

```text
display interface brief
display ip interface brief
display current-configuration
display ip routing-table
```

### 1.2 分层排障法

| 层次 | 核心对象 | 典型问题 |
|---|---|---|
| 物理层 | 接口、模块、速率、双工、光功率 | 接口 down、丢包、CRC |
| 二层 | VLAN、MAC、Trunk、STP、聚合 | 同网段不通、广播异常 |
| 三层 | ARP、IP、路由、邻居 | 跨网段不通、邻居不起 |
| 四层 | TCP/UDP、端口、NAT | 某业务不通但 ping 通 |
| 应用层 | DNS、HTTP、认证、API | 网通但业务不可用 |

### 1.3 三个关键问题

每次故障都问：

1. 是所有业务都不通，还是某一类业务不通？
2. 是所有用户都不通，还是某个网段/某台设备不通？
3. 是一直不通，还是最近变更后不通？

---

## 2. 快速排障总表

| 现象 | 最先怀疑 | 先查什么 |
|---|---|---|
| 接口不通 | 物理/接口状态 | `display interface brief` |
| 同 VLAN 不通 | VLAN/端口类型/MAC | `display vlan` `display mac-address` |
| 跨 VLAN 不通 | Vlanif/网关/ACL | `display ip interface brief` |
| OSPF 邻居不起 | Area/认证/MTU/IP | `display ospf peer` |
| BGP 邻居不起 | AS/可达性/源接口 | `display bgp peer` |
| 有邻居但没路由 | 过滤/策略/宣告缺失 | `display routing-table` |
| MPLS VPN 不通 | IGP/LDP/MP-BGP/VRF | `display mpls ldp session` |
| Internet 不通 | 缺省路由/NAT/ACL | `display ip routing-table` `display nat session` |
| 无线能连但不能上网 | 认证/NAT/DHCP/DNS | `display ip pool` |
| 某应用慢 | QoS/丢包/拥塞/路径绕行 | 接口统计+路由路径 |

---

## 3. 物理层故障

### 场景 1：接口 down/down

#### 现象

- `display interface brief` 显示接口 down
- 无法 ping 通直连接口

#### 可能原因

- 网线/光纤没接好
- 模块故障
- 对端接口 shutdown
- 速率/双工不匹配

#### 验证命令

```text
display interface brief
display interface GigabitEthernet 0/0/1
```

#### 修复动作

- 检查物理连接
- `undo shutdown`
- 检查对端接口状态
- 统一速率与双工

#### 专家技巧

- 先看接口是否 up，再看协议是否 up
- `up/down` 和 `down/down` 的含义不同

### 场景 2：接口 up 但丢包严重

#### 可能原因

- CRC 错误
- 双工不一致
- 光模块质量差
- 上联拥塞

#### 验证命令

```text
display interface GigabitEthernet 0/0/1
```

重点看：

- CRC
- input error
- output error
- discard

#### 修复动作

- 更换线缆/模块
- 对齐速率双工
- 检查链路利用率

---

## 4. 二层故障

### 场景 3：同 VLAN 主机不通

#### 现象

- PC1 与 PC2 理论上同网段，但互 ping 不通

#### 可能原因

- 接口没进同一个 VLAN
- 接口还是 trunk/hybrid 但接法不对
- MAC 没学习到
- STP 阻塞了异常端口

#### 验证命令

```text
display vlan
display port vlan
display mac-address
display stp brief
```

#### 修复动作

- 确认接口类型是 access
- 确认 `port default vlan`
- 确认 trunk 放行 VLAN
- 排查是否误入隔离端口

#### 专家技巧

- 同 VLAN 不通先查二层，不要急着查路由
- `display mac-address` 是判断二层学习是否正常的关键

### 场景 4：跨交换机同 VLAN 不通

#### 可能原因

- trunk 没放行对应 VLAN
- trunk 两端模式不一致
- 聚合口成员不一致

#### 验证命令

```text
display interface brief
display port vlan
display eth-trunk 1
```

#### 修复动作

- 在 trunk 口补 `allow-pass vlan`
- 聚合口两端链路策略一致

---

## 5. 三层故障

### 场景 5：跨 VLAN 不通

#### 现象

- VLAN10 能访问本地，但访问 VLAN20 不通

#### 可能原因

- Vlanif 没有 IP
- Vlanif 没有起来
- PC 网关配置错误
- ACL 拦截

#### 验证命令

```text
display ip interface brief
display current-configuration interface Vlanif 10
display current-configuration interface Vlanif 20
display acl all
```

#### 修复动作

- 给 Vlanif 配 IP
- 确保对应 VLAN 有活跃端口，Vlanif 才会 up
- 修正终端网关
- 检查接口 ACL

### 场景 6：静态路由配置了但不通

#### 可能原因

- 下一跳不可达
- 返回路由缺失
- 路由掩码写错

#### 验证命令

```text
display ip routing-table
ping x.x.x.x
tracert x.x.x.x
```

#### 修复动作

- 确保下一跳直连可达
- 补对端回程路由
- 检查掩码

#### 专家技巧

- 路由“去得了但回不来”非常常见
- 任意互通问题都要双向看

---

## 6. OSPF 故障

根据华为官方 `display ospf peer`、`display ospf interface` 等命令，OSPF 排障优先看邻居关系和接口参数。citeturn0search0

### 场景 7：OSPF 邻居不起

#### 可能原因

- IP 不通
- Area 不一致
- Hello/Dead 时间不一致
- 认证不一致
- MTU 不一致
- Router ID 冲突

#### 验证命令

```text
display ospf peer
display ospf interface
display current-configuration | include ospf
display ip interface brief
```

#### 修复动作

- 确认底层三层可达
- 对齐 Area
- 对齐定时器
- 对齐认证
- 对齐 MTU 或做相应调整

#### 排障顺序

1. 接口 up 吗
2. IP 通吗
3. 邻居状态是什么
4. 区域和认证对吗
5. MTU 和网络类型对吗

### 场景 8：OSPF 邻居 Full，但没学到路由

#### 可能原因

- network 未宣告
- 路由过滤
- 汇总影响
- 引入缺失

#### 验证命令

```text
display ospf routing
display ip routing-table protocol ospf
display current-configuration | include import-route
```

#### 修复动作

- 补正确网段宣告
- 检查 area 设计与汇总
- 检查路由策略

---

## 7. BGP 故障

### 场景 9：BGP 邻居建立失败

#### 可能原因

- 对端 AS 配错
- 源地址不对
- 对端不可达
- Loopback 建邻未指定源接口
- TCP 179 被拦截

#### 验证命令

```text
display bgp peer
display current-configuration | include bgp
display ip routing-table
ping x.x.x.x
```

#### 修复动作

- 修正 `peer x.x.x.x as-number`
- 如果是 loopback 建邻，补 `connect-interface`
- 确保有到对端 loopback 的路由

### 场景 10：BGP 邻居起了，但没路由

#### 可能原因

- 本地没宣告 `network`
- 宣告前缀不在路由表
- route-policy 过滤掉了
- next-hop 不可达

#### 验证命令

```text
display bgp routing-table
display ip routing-table
display current-configuration | include route-policy
```

#### 修复动作

- 确保要宣告的前缀先存在于本地路由表
- 放开错误策略
- 修正 next-hop

#### 专家技巧

- BGP 的路由问题，很多时候不是“协议没起”，而是“策略把路由改没了”

---

## 8. MPLS / LDP / VPN 故障

### 场景 11：LDP 邻居不起

#### 可能原因

- 接口未开启 MPLS/LDP
- IGP 不通
- LSR-ID 问题

#### 验证命令

```text
display mpls ldp session
display mpls lsp
display ip routing-table
```

#### 修复动作

- 在接口上补 `mpls`、`mpls ldp`
- 确保 IGP 打通

### 场景 12：MPLS VPN 不通

#### 可能原因

- VRF 未绑定接口
- RD/RT 配错
- MP-BGP VPNv4 邻居没建好
- CE-PE 没学到客户路由
- 标签不通

#### 验证命令

```text
display ip vpn-instance
display bgp vpnv4 all peer
display bgp vpnv4 all routing-table
display ip routing-table vpn-instance VPN-A
display mpls forwarding-table
```

#### 修复动作

- 检查接口绑定 VRF
- 检查 RT import/export
- 检查 MP-BGP 激活
- 检查 PE-CE 路由学习

#### 专家技巧

- VPN 不通不要乱查
- 固定顺序：IGP -> LDP -> MP-BGP -> VRF -> 标签

---

## 9. NAT / DHCP / Internet 出口故障

### 场景 13：内网能到网关，但不能上网

#### 可能原因

- 缺省路由没配
- NAT 没生效
- ACL 没匹配内网地址
- 出口接口没做 NAT

#### 验证命令

```text
display ip routing-table
display nat session all
display nat outbound
display acl 2001
```

#### 修复动作

- 补默认路由
- 检查 NAT 调用 ACL
- 检查出口口是否调用 NAT

### 场景 14：终端拿不到 DHCP 地址

#### 可能原因

- DHCP 未开启
- 地址池写错
- 网关接口未做 DHCP 选择
- 中继缺失

#### 验证命令

```text
display ip pool
display dhcp server ip-in-use
display current-configuration | include dhcp
```

#### 修复动作

- 开启 `dhcp enable`
- 修正地址池
- 接口补 `dhcp select interface`

---

## 10. 无线 / 园区常见问题

### 场景 15：无线已关联，但无法上网

#### 可能原因

- DHCP 失败
- VLAN 映射错误
- Portal/认证未通过
- 出口 NAT 或 DNS 问题

#### 验证思路

1. 客户端有地址吗
2. 网关能通吗
3. DNS 能解析吗
4. 是否通过认证

#### 典型命令方向

- 查看地址池使用
- 查看 VLAN/Vlanif
- 查看认证状态
- 查看出口 NAT

### 场景 16：用户漫游后业务异常

#### 可能原因

- 策略未随用户迁移
- 认证状态同步异常
- Overlay/EVPN 控制面不稳定

#### 专家技巧

- 园区问题不要只看一台接入交换机
- 要看“用户身份、位置、业务策略、控制器状态、Overlay 路径”

---

## 11. 性能与质量问题

### 场景 17：ping 通，但业务很慢

#### 可能原因

- 丢包
- MTU 问题
- QoS 没生效
- 路由绕行
- CPU/接口拥塞

#### 验证命令

```text
display interface GigabitEthernet 0/0/1
display cpu-usage
display ip routing-table
```

#### 修复动作

- 看接口丢弃与利用率
- 检查大流量是否挤占链路
- 验证路径是否绕远
- 检查队列/QoS 策略

### 场景 18：高峰期偶发中断

#### 常见思路

- 查链路是否拥塞
- 查 STP/OSPF/BGP 是否频繁重收敛
- 查设备 CPU/内存是否打满
- 查是否有环路或广播风暴

---

## 12. 变更后的故障

### 场景 19：改完配置后全网部分异常

#### 高级处理流程

1. 先冻结变更
2. 记录故障时间点
3. 对比变更前后配置
4. 确认是否需要回退

#### 建议命令

```text
display current-configuration
display logbuffer
display saved-configuration
```

#### 专家技巧

- 网络故障很多不是技术不懂，而是变更控制差
- 高级工程师一定要有“变更前基线、变更中验证、变更后回退预案”

---

## 13. 排障模板

建议你以后每次故障都按这个模板记录：

### 故障记录模板

| 项目 | 内容 |
|---|---|
| 故障时间 |  |
| 影响范围 |  |
| 业务现象 |  |
| 最近变更 |  |
| 初步判断层次 | 物理/二层/三层/应用 |
| 核心命令输出 |  |
| 根因分析 |  |
| 修复动作 |  |
| 回退动作 |  |
| 复盘结论 |  |

---

## 14. 高级专家的故障思维

### 14.1 永远先问“最小闭环”

例如跨 VLAN 不通，不要一上来就查全网。  
先看：

- PC IP 对不对
- 网关 Vlanif 对不对
- 同交换机是否可达
- 再扩大到 trunk、路由、策略

### 14.2 学会“缩圈”

排障不是一次定位，是不断缩小问题范围：

1. 是主机问题还是网络问题
2. 是接入问题还是骨干问题
3. 是单点问题还是全局问题
4. 是控制面问题还是数据面问题

### 14.3 高级技巧

- 任何故障都先看“最近变更”
- 任何协议都要有“邻居、路由、转发”三视角
- 任何业务都要有“去程、回程”双向思维
- 任何现象都要区分“完全不通”和“部分不通”

---

## 15. 常用排障命令索引

| 类别 | 命令 |
|---|---|
| 接口 | `display interface brief` |
| IP 接口 | `display ip interface brief` |
| VLAN | `display vlan` |
| MAC | `display mac-address` |
| STP | `display stp brief` |
| 路由 | `display ip routing-table` |
| OSPF | `display ospf peer` `display ospf routing` |
| BGP | `display bgp peer` `display bgp routing-table` |
| MPLS | `display mpls ldp session` `display mpls forwarding-table` |
| NAT | `display nat session all` |
| DHCP | `display ip pool` |
| CPU | `display cpu-usage` |
| 日志 | `display logbuffer` |

---

## 16. 结语

真正的高级网络专家，不是“知道很多命令”，而是：

- 看到现象就知道从哪一层切入
- 不被表象带偏
- 能快速缩小范围
- 能把排障过程讲清楚
- 能把临时修复转化成长期优化

学网络到后面，拼的是：

- 方法
- 稳定性
- 结构化思维
- 复盘能力

如果你把这份手册配合实验一天一天过，你会明显从“会配设备”进入“会排网络问题”的阶段。

