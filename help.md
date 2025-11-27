# 校园跑新手指南

项目仓库：[iOSRealRun-cli-18](https://github.com/ChenyuHeee/iOSRealRun-cli-18)

本指南面向第一次接触命令行的同学，按照下面的流程一步步操作即可让 iOS 设备开始“模拟跑步”。使用过程中如遇报错，请耐心核对每个步骤是否完成、指令是否输入正确。

**注意：**

- 一定要先开始模拟跑步，然后再在浙大体艺中开始运动。否则可能出现起点在东教的情况。
- 连接数据线前请确保设备已解锁，仅连接一台 iPhone 或 iPad。建议使用原厂数据线。
- 若更换数据线或电脑 USB 口，建议重新执行挂载与启动步骤。
- 任何一步失败时先不要慌，按照顺序重新检查上一条是否完成。

## Windows 用户流程

1. **准备必备软件**
   1. 前往 [python.org](https://www.python.org/downloads/) 下载最新的 Python 3（推荐 3.10 及以上，测试环境为 3.13）。安装向导中务必勾选 `Add python.exe to PATH` 和 `Install pip`。
   2. 安装完成后，打开开始菜单，输入 `cmd`，选择“命令提示符”并输入：
      ```shell
      python --version
      pip --version
      ```
      两个命令都能正确显示版本号才表示安装成功。
   3. 若尚未安装 Git，可从 [git-scm.com](https://git-scm.com/download/win) 下载；不熟悉 Git 也可以直接下载仓库的 ZIP 压缩包。
   4. 通过 Microsoft Store（推荐）或苹果官网安装最新的 iTunes，并首次启动一次以确保苹果驱动正确加载。

2. **获取项目代码**
   1. 如果使用 Git：在资源管理器中定位到希望存放项目的文件夹，地址栏输入 `cmd` 并回车，随后执行：
      ```shell
      git clone https://github.com/ChenyuHeee/iOSRealRun-cli-18.git
      cd iOSRealRun-cli-18
      ```
   2. 如果下载 ZIP：将压缩包解压后右键空白处选择“在终端中打开”或地址栏输入 `cmd`，然后 `cd` 到解压出来的 `iOSRealRun-cli-18` 文件夹，例如：
      ```shell
      cd "%USERPROFILE%\Downloads\iOSRealRun-cli-18"
      ```

3. **创建并启用虚拟环境（推荐）**
   1. 以管理员身份打开终端：点击开始菜单 → 输入 `cmd` → 右键“命令提示符”选择“以管理员身份运行”。
   2. 在管理员终端中执行：
      ```shell
      python -m venv .venv
      .\.venv\Scripts\activate
      ```
      若看到命令行前缀出现 `(.venv)` 表示激活成功。以后重新打开终端时需要再次运行第二条命令激活环境。

4. **安装 Python 依赖**
   1. 仍在项目目录下执行：
      ```shell
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      ```
      如果提示连接失败或版本不可用，请暂时关闭国内镜像源（可增加 `--no-cache-dir`）。

5. **准备配置文件**
   1. 用记事本或 VS Code 打开 `config.yaml`：
      - `v` 表示跑步速度（单位 m/s），可根据需要调整。
      - `routeConfig` 指向使用的路线文件，可在 `HNroute.txt`、`YQroute.txt`、`ZJGroute.txt` 中选择其一，也可自行复制修改；文件内是经纬度数组，保持格式不变。
   2. 如果你修改了路线文件，请确保文本内容仍然是合法的 JSON 风格字典数组，例如：`{"lat": "31.23", "lng": "121.47"}`。

6. **连接设备并挂载开发者镜像**
   1. 使用原装数据线连接 iPhone/iPad，解锁设备并在提示时选择“信任”。
   2. 以普通用户身份打开终端（可与管理员终端分开），如果命令行前缀没有 `(.venv)`，请先运行 `.\.venv\Scripts\activate`，然后执行：
      ```shell
      pymobiledevice3 mounter auto-mount
      ```
      首次运行会自动下载并挂载开发者镜像，结束后返回 `Mounted developer image` 类似提示即可。

7. **启动模拟跑步**
   1. 回到“以管理员身份”运行的终端窗口（同样需要激活虚拟环境），确认当前目录是项目根目录，可先输入 `cd` 查看路径，若不在项目文件夹内请执行 `cd C:\Users\你的用户名\Downloads\iOSRealRun-cli-18`（将路径替换为你保存项目的真实位置）。
   2. 执行：
      ```shell
      python main.py
      ```
   3. 终端会提示“已开始模拟跑步...按 Ctrl+C 退出”。保持窗口开启即可。若提示未检测到设备，请确认设备仍然解锁、数据线连接稳定、iTunes 已开启一次。

8. **结束与收尾**
   1. 完成后在终端按 `Ctrl+C` 正常退出，直到看到 `Bye`。
   2. 如设备定位未恢复，可在手机端关闭“飞行模式”或重启手机。
   3. 若使用虚拟环境，可输入 `deactivate` 退出。

9. **常见问题（Windows）**
   - `pip` 报权限错误：确认终端是以管理员启动，或将项目放在非系统盘路径。
   - `No device connected`：拔插数据线、重启 iTunes，并重新执行第 6 步。
   - `ModuleNotFoundError`: 重新激活虚拟环境并运行依赖安装命令。

## macOS 用户流程

1. **准备必备软件**
   1. 按 `Command + Space` 调出 Spotlight，输入 `Terminal` 并回车打开“终端”，执行：
      ```shell
      python3 --version
      pip3 --version
      ```
      若系统未自带或版本偏旧，建议通过 [Homebrew](https://brew.sh/) 安装：
      ```shell
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      brew install python@3.13
      ```
      安装完成后重新打开终端。
   2. 运行 `xcode-select --install` 安装命令行工具（未安装时会弹窗提示）。

2. **获取项目代码**
   1. 若使用 Git：
      ```shell
      git clone https://github.com/ChenyuHeee/iOSRealRun-cli-18.git
      cd iOSRealRun-cli-18
      ```
   2. 若下载 ZIP：用 Finder 解压后，右键项目文件夹选择“在终端中打开”。

3. **创建并启用虚拟环境（推荐）**
   1. 执行：
      ```shell
      python3 -m venv .venv
      source .venv/bin/activate
      ```
      提示符前出现 `(.venv)` 说明激活成功。

4. **安装 Python 依赖**
   ```shell
   python3 -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
   如遇权限或 SSL 报错，请先确认虚拟环境已激活；若仍无法安装，可先执行 `deactivate` 退出虚拟环境，再运行 `sudo python3 -m pip install -r requirements.txt`，随后重新 `source .venv/bin/activate`，避免直接在虚拟环境内使用 `sudo pip`。

5. **准备配置文件**
   1. 使用文本编辑器打开 `config.yaml` 调整速度与路线，规则与 Windows 章节相同。
   2. 自定义路线时，保持经纬度字段为字符串或数字，不要删除逗号和花括号。

6. **连接设备并挂载开发者镜像**
   1. 用数据线连接 iPhone/iPad，解锁并在 Mac 上的提示框中选择“信任”。
   2. 在激活了虚拟环境的终端中执行（如提示符前没有 `(.venv)`，请先运行 `source .venv/bin/activate`）：
      ```shell
      sudo pymobiledevice3 mounter auto-mount
      ```
      需要输入电脑密码。若提示权限不足，可在“系统设置 > 隐私与安全性 > 完整磁盘访问”中为终端授予权限后重试。

7. **启动模拟跑步**
   1. 确认当前目录仍在项目根目录，可执行 `pwd` 查看路径；若末尾不是 `iOSRealRun-cli-18`，请执行 `cd ~/路径/iOSRealRun-cli-18`（将 `~/路径/` 替换成你解压或克隆时的实际位置），然后在同一终端执行：
      ```shell
      sudo python3 main.py
      ```
   2. 终端出现“已开始模拟跑步...”即表示程序正在向设备推送虚拟定位。
   3. 运行期间请保持设备屏幕常亮（可打开屏幕保持设置），以免连接断开。

8. **结束与收尾**
   1. 结束时按 `Ctrl+C`，看到 `Bye` 后再关闭终端窗口。
   2. 若定位仍指向跑道，可关闭“飞行模式”或重启设备恢复。
   3. 使用虚拟环境的用户可执行 `deactivate` 退出。

9. **常见问题（macOS）**
   - `Operation not permitted`：在“系统设置 > 隐私与安全性 > 开发者工具”或“完整磁盘访问”中添加 Terminal 并重新运行 `sudo` 命令。
   - `No module named ...`：确认虚拟环境已激活，重新安装依赖。
   - `Failed mounting developer image`：拔掉数据线重新插入，确保设备已解锁，并再次执行第 6 步。

> 小贴士：如果想在多台设备或不同路线之间切换，建议为不同场景分别备份 `config.yaml` 或对应的路线文件，运行前替换即可。