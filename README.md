# iOSRealRun-cli-18

在电脑上模拟 iPhone/iPad GPS 定位，实现虚拟跑步 —— 沿真实路线自动模拟运动轨迹。

基于 [iOSRealRun-cli-17](https://github.com/iOSRealRun/iOSRealRun-cli-17) 修改，适配 iOS 18，更新了 [pymobiledevice3](https://github.com/doronz88/pymobiledevice3) 依赖。

---

## 原理

1. 通过 `pymobiledevice3` 与 iOS 设备建立 USB 远程调试连接
2. 利用 Apple DVT (Developer Tools) 框架的 `LocationSimulation` 注入虚假定位
3. 从路线文件读取坐标 → 按速度插值 → 加随机偏移模拟真实运动 → 持续发送到设备

## 测试环境

| 项目 | 版本 |
|------|------|
| 操作系统 | macOS, Windows 11 |
| Python | 3.11+ |
| iOS | 18+ |

## 前置准备

1. **Windows 需要安装 iTunes**（提供设备通信驱动）
2. iOS 设备系统版本 ≥ 18
3. 已安装 Python 3 和 pip
4. **只能有一台 iOS 设备连接电脑**
5. 需要管理员/root 权限（创建 tun 设备）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 连接设备

将 iPad/iPhone 通过 USB 连接到电脑，解锁并点击"信任"。

### 3. 挂载 Developer Disk Image

```bash
pymobiledevice3 mounter auto-mount
```

### 4. 运行

**Windows（管理员权限）：**

```powershell
python main.py
```

**macOS：**

```bash
sudo python3 main.py
```

### 5. 退出

按 `Ctrl + C` 终止程序。**请务必用 Ctrl+C 退出**，否则定位不会自动恢复。如果定位未恢复，重启手机即可。

## 配置

编辑 `config.yaml`：

```yaml
v: 4.8                    # 速度 (m/s)，默认约 4 min/km 配速
routeConfig: "ZJGroute.txt"  # 路线文件
```

### 路线文件

仓库内置三条路线（坐标从百度地图取的 BD-09，程序自动转为 WGS-84）：

| 文件 | 路线 |
|------|------|
| `ZJGroute.txt` | 浙大紫金港东操（默认） |
| `YQroute.txt` | 浙大玉泉 |
| `HNroute.txt` | 浙大海宁 |

## 项目结构

```
iOSRealRun-cli-18/
├── main.py                  # 入口（支持 -m 限时运行）
├── run.py                   # 核心：坐标转换、插值、定位注入
├── config.py                # 配置加载
├── config.yaml              # 速度 / 路线配置
├── requirements.txt         # Python 依赖
├── start.bat                # 一键启动脚本（推荐）
├── start.ps1                # PowerShell 版启动脚本
│
├── init/
│   ├── init.py              # 初始化
│   ├── tunnel.py            # USB 隧道
│   └── route.py             # 路线读取
│
├── driver/
│   └── connect.py           # 设备连接
│
└── util/
    └── route.py             # 路线工具
```

## 自动停止

支持限定运行时长，到点自动停止并恢复真实定位：

```bash
python main.py -m 30       # 跑 30 分钟后自动停止
python main.py              # 无限运行（需 Ctrl+C 手动停止）
```

### 一键启动脚本

**`start.bat`（推荐）** — 双击运行，自动提权 → 挂载镜像 → 启动 → 到时停止：

| 命令 | 说明 |
|------|------|
| 双击 `start.bat` | 默认跑 **30 分钟** |
| `start.bat -m 45` | 跑 45 分钟 |
| `start.bat -m 0` | 无限运行 |
| `start.bat -m 20 -n` | 跑 20 分钟，跳过挂载 |

**`start.ps1`** — PowerShell 版本（功能同上）

---

## 升级记录

### pymobiledevice3 4.20.20 → 9.19.0

原项目锁定的 `pymobiledevice3==4.20.20` 在 iOS 新版上 `LocationSimulation` 注入会超时。升级到 9.19.0 后涉及以下破坏性变更：

#### 波及文件及修改

| 文件 | 变更 |
|------|------|
| `run.py` | `DvtSecureSocketProxyService` → `DvtProvider`（async context manager）；`LocationSimulation.set()` 改为 `async`；同步 `time.sleep` 改为 `asyncio.sleep` |
| `init/init.py` | `init()` 改为 `async`，适配 `connect` 模块 async 化 |
| `driver/connect.py` | `create_using_usbmux()` 改为 `await`；`developer_mode_status` 属性 → `get_developer_mode_status()` 方法（async）；`AmfiService` 方法均为 async |
| `main.py` | 新增 `argparse` 支持 `-m`/`--minutes` 参数；`.init()` → `await`；捕获 `asyncio.TimeoutError` 实现自动停止 |
| `requirements.txt` | `pymobiledevice3>=9.19.0` |

#### 核心 API 变化

```python
# 旧版 (4.20.20)
from pymobiledevice3.services.dvt.dvt_secure_socket_proxy import DvtSecureSocketProxyService
dvt = DvtSecureSocketProxyService(rsd)
dvt.perform_handshake()
LocationSimulation(dvt).set(lat, lng)                # 同步

# 新版 (9.19.0)
from pymobiledevice3.services.dvt.instruments.dvt_provider import DvtProvider
async with DvtProvider(rsd) as dvt:
    async with LocationSimulation(dvt) as loc_sim:
        await loc_sim.set(lat, lng)                   # async
```

---

## 常见问题

**"Failed to connect to usbmuxd socket"**
→ 没有安装 iTunes，或 Apple Mobile Device Service 未运行。

**"No device connected"**
→ 确保设备已解锁并点击"信任"，重插 USB 线试试。

**定位没恢复**
→ 重启手机即可恢复真实定位。

## 致谢

- [iOSRealRun](https://github.com/iOSRealRun/iOSRealRun-cli-17) - 原项目
- [pymobiledevice3](https://github.com/doronz88/pymobiledevice3) - iOS 远程调试库
