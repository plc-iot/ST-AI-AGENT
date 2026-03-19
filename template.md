# template.st 框架说明文档

## 1. 概述

template.st 是一个用于 AI 自动生成 ST 程序的框架模板，包含了 TCP 通信、调试指令处理、OTA 升级配置和系统信息管理等功能。该模板为 PLC 程序提供了基础的通信和调试能力，可作为开发 IoT 应用的起点。

## 2. 框架结构

 template.st 由以下几个主要部分组成：

### 2.1 时间获取函数

```st
FUNCTION GETTIMEOFDAY : TIME
  VAR_INPUT
    EN : BOOL := TRUE;
  END_VAR
  {GETTIMEOFDAY = __CURRENT_TIME;}
END_FUNCTION
```

**说明**：GETTIMEOFDAY 函数获取自1970年1月1日00:00:00 UTC以来的当前时间，返回 TIME 类型的值。这个函数的功能和C语言的 gettimeofday 相同。

### 2.2 程序主体

```st
PROGRAM TEMPLATE
  VAR
    TCP0 : TCP_CLIENT;
    RX0 : TCP_RX;
    RX1 : TCP_RX;
    TX0 : TCP_TX;
    VN  : STRING;
    VV  : STRING;
    SV  : SETV;
    GV  : GETV;
  END_VAR

  TCP0(SVR := '192.168.31.155', PORT := 5000);
  RX0(EN := TCP0.S, BIN := FALSE, C := TCP0.C, MSG := 'GETV[[@VN]]');
  RX1(EN := TCP0.S,BIN := FALSE,C := TCP0.C,MSG := 'SETV[[@VN],[@VV]]');
  SV(EN := RX1.R,M := VN,S := VV);
  GV(EN := RX0.R OR SV.ENO,M := VN);
  TX0(EN := TCP0.S,BIN := FALSE,C := TCP0.C,MSG := '[@VN]:[@GV.S]',T := GV.ENO);

END_PROGRAM
```

### 2.3 配置部分

```st
CONFIGURATION CONFIG0
  VAR_GLOBAL
    UPG_CFG : STRING := 'UPGRADE_CONFIG@[UP,SVR]';
    OTA_CFG : STRING := 'OTA_CONFIG@[OTA,SVR]';
    UP  : BOOL := FALSE;
    OTA : BOOL := FALSE;
    SVR : STRING := 'http server';
  END_VAR
  VAR_GLOBAL
    SYS_CFG : STRING := 'SYS_SETTING@[MAC:MACV,VER:VM]';
    MACV : ULINT;
    VM : UDINT;
  END_VAR
  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM instance0 WITH task0 : TEMPLATE;
  END_RESOURCE
END_CONFIGURATION
```

## 3. 功能模块说明

### 3.1 TCP 客户端功能（TCP_CLIENT）

**功能**：创建 TCP 客户端连接，用于连接调试测试终端服务器。

**参数**：
- `SVR`（输入，STRING）：服务器地址，默认为 '192.168.31.155'
- `PORT`（输入，UINT）：服务器端口，默认为 5000
- `S`（输出，BOOL）：连接状态信号，连接成功时为 TRUE
- `C`（输出，INT）：连接句柄

**工作原理**：
- 初始化时创建 TCP 套接字并尝试连接到指定服务器
- 连接成功后，`S` 变为 TRUE，`C` 输出连接句柄
- 支持网络状态检测和自动重连

### 3.2 调试指令接收（TCP_RX）

**功能**：通过 TCP 接收调试指令，支持消息解析和变量赋值。

**参数**：
- `EN`（输入，BOOL）：使能信号，使用 TCP0.S 作为使能条件
- `BIN`（输入，BOOL）：二进制模式标志，默认为 FALSE（文本模式）
- `C`（输入，INT）：连接句柄，使用 TCP0.C
- `MSG`（输入，STRING）：消息模板，用于解析接收到的消息
- `R`（输出，BOOL）：接收完成信号

**实例**：
- `RX0`：用于接收 `GETV[变量名]` 指令
- `RX1`：用于接收 `SETV[变量名,变量值]` 指令

### 3.3 变量操作功能块

#### 3.3.1 SETV 功能块

**功能**：设置变量的值，支持各种数据类型。

**参数**：
- `EN`（输入，BOOL）：使能信号，使用 RX1.R 作为使能条件
- `M`（输入，STRING）：变量名称，使用 VN 变量
- `S`（输入，STRING）：变量值（字符串形式），使用 VV 变量
- `SUCCESS`（输出，BOOL）：成功信号

#### 3.3.2 GETV 功能块

**功能**：获取变量的值，支持各种数据类型。

**参数**：
- `EN`（输入，BOOL）：使能信号，使用 RX0.R OR SV.ENO 作为使能条件
- `M`（输入，STRING）：变量名称，使用 VN 变量
- `S`（输出，STRING）：变量值（字符串形式）
- `SUCCESS`（输出，BOOL）：成功信号

### 3.4 调试信息返回（TCP_TX）

**功能**：通过 TCP 发送调试信息，支持消息模板和变量替换。

**参数**：
- `EN`（输入，BOOL）：使能信号，使用 TCP0.S 作为使能条件
- `BIN`（输入，BOOL）：二进制模式标志，默认为 FALSE（文本模式）
- `C`（输入，INT）：连接句柄，使用 TCP0.C
- `MSG`（输入，STRING）：消息模板，支持使用 [@变量名] 格式嵌入变量
- `T`（输入，BOOL）：触发信号，使用 GV.ENO 作为触发条件

**消息模板**：`'[@VN]:[@GV.S]'`，用于返回变量名和其值

### 3.5 设备当前时间获取（GETTIMEOFDAY）

**功能**：获取自1970年1月1日00:00:00 UTC以来的当前时间，返回 TIME 类型的值。

**参数**：
- `EN`（输入，BOOL）：使能信号，默认为 TRUE

**返回值**：
- `TIME` 类型：自1970年1月1日00:00:00 UTC以来的当前时间（以秒和微秒表示）

**说明**：
GETTIMEOFDAY 函数返回的时间戳可以用于：
- 计算时间差
- 实现精确的时间戳记录
- 同步不同设备的时间
- 实现日志记录和事件时间戳

**使用示例**：
```st
// 获取时间戳并存储到变量中
VAR
    Timestamp : TIME;
END_VAR

Timestamp := GETTIMEOFDAY();

// 使用时间戳进行时间差计算
VAR
    StartTime : TIME;
    EndTime : TIME;
    Duration : TIME;
END_VAR

StartTime := GETTIMEOFDAY();
// 执行一些操作...
EndTime := GETTIMEOFDAY();
Duration := EndTime - StartTime;

// 使用当前时间进行计时或定时操作
VAR
    CurrentTime : TIME;
    SomeTime : TIME;
END_VAR

CurrentTime := GETTIMEOFDAY();
IF CurrentTime > SomeTime THEN
    // 执行定时任务
END_IF;
```

## 4. 配置项说明

### 4.1 升级相关配置

**UPG_CFG**：PLC 程序升级配置
- 格式：`UPGRADE_CONFIG@[UP,SVR]`
- 参数：
  - `UP`：升级触发信号，BOOL 类型，默认为 FALSE
  - `SVR`：升级服务器地址，STRING 类型，默认为 '192.168.31.155'

**OTA_CFG**：ESP 固件升级配置
- 格式：`OTA_CONFIG@[OTA,SVR]`
- 参数：
  - `OTA`：升级触发信号，BOOL 类型，默认为 FALSE
  - `SVR`：升级服务器地址，STRING 类型，默认为 '192.168.31.155'

### 4.2 系统信息配置

**SYS_CFG**：系统信息配置
- 格式：`SYS_SETTING@[MAC:MACV,VER:VM]`
- 参数：
  - `MAC:MACV`：设备 MAC 地址，使用 MACV 变量（ULINT 类型）
  - `VER:VM`：设备版本号，使用 VM 变量（UDINT 类型）

## 5. 通信流程

### 5.1 GETV 指令处理流程

1. 客户端发送 `GETV[变量名]` 指令
2. `RX0` 功能块接收并解析指令，提取变量名到 `VN` 变量
3. `RX0.R` 变为 TRUE，触发 `GV` 功能块
4. `GV` 功能块根据 `VN` 变量获取对应变量的值
5. `GV.ENO` 变为 TRUE，触发 `TX0` 功能块
6. `TX0` 功能块发送 `变量名:变量值` 格式的响应

### 5.2 SETV 指令处理流程

1. 客户端发送 `SETV[变量名,变量值]` 指令
2. `RX1` 功能块接收并解析指令，提取变量名到 `VN` 变量，提取变量值到 `VV` 变量
3. `RX1.R` 变为 TRUE，触发 `SV` 功能块
4. `SV` 功能块根据 `VN` 和 `VV` 变量设置对应变量的值
5. `SV.ENO` 变为 TRUE，触发 `GV` 功能块
6. `GV` 功能块获取刚设置的变量值
7. `GV.ENO` 变为 TRUE，触发 `TX0` 功能块
8. `TX0` 功能块发送 `变量名:变量值` 格式的响应

## 6. 使用方法

### 6.1 基本使用

1. **使用框架模板生成ST程序**：
   - 复制 `template.st` 文件并重命名为您的程序名
   - 将文件中的 `PROGRAM TEMPLATE` 替换为 `PROGRAM 您的程序名`
   - 将 `PROGRAM instance0 WITH task0 : TEMPLATE;` 替换为 `PROGRAM instance0 WITH task0 : 您的程序名;`

2. **配置网络参数**：
   - 修改 `TCP0` 的 `SVR` 和 `PORT` 参数，设置为实际的调试服务器地址和端口

3. **编译和下载**：
   - 编译并下载程序到 PLC 设备

4. **测试通信**：
   - 启动调试服务器，等待 PLC 连接
   - 发送调试指令进行测试：
     - 发送 `GETV[变量名]` 获取变量值
     - 发送 `SETV[变量名,变量值]` 设置变量值

### 6.2 配置升级功能

1. 修改 `SVR` 变量为实际的升级服务器地址
2. 设置 `UP` 或 `OTA` 变量为 TRUE 触发升级
3. 升级服务器需要提供相应的固件文件

### 6.3 扩展系统信息

可以在 `SYS_CFG` 中添加更多系统信息：

```st
SYS_CFG : STRING := 'SYS_SETTING@[MAC:MACV,VER:VM,IP:IP_ADDR]';
IP_ADDR : STRING;
```

## 7. 扩展指南

### 7.1 添加新的调试指令

1. 添加新的 `TCP_RX` 功能块实例
2. 定义消息模板和相关变量
3. 添加对应的处理逻辑
4. 更新 `TX0` 的消息模板以支持新指令的响应

### 7.2 集成其他通信协议

可以根据需要集成其他通信协议，如 MQTT、MODBUS 等：

```st
// 添加 MQTT 通信
VAR
    MqttClient: WIFI_MQTT;
    MqttTx: MSG_TX;
    MqttRx: MSG_RX;
END_VAR

// 初始化 MQTT
MqttClient(SSID:="MyWiFi", PSW:="password", SVR:="mqtt.example.com");

// 发送 MQTT 消息
MqttTx(TOPIC:="plc/data", MSG:="Value: [@Variable]", T:=SendTrigger);

// 接收 MQTT 消息
MqttRx(TOPIC:="plc/commands", MSG:="COMMAND:[@Command]");
```

### 7.3 添加控制逻辑

可以在模板基础上添加具体的控制逻辑：

```st
// 添加控制逻辑
VAR
    SensorValue: REAL;
    Setpoint: REAL := 50.0;
    Output: REAL;
    PID_Controller: PID;
END_VAR

// PID 控制
PID_Controller(AUTO:=TRUE, PV:=SensorValue, SP:=Setpoint, 
              KP:=1.0, TR:=10.0, TD:=2.0, CYCLE:=T#100ms);
Output := PID_Controller.XOUT;
```

## 8. 注意事项

1. **网络连接**：确保 PLC 设备能够访问指定的服务器地址
2. **端口配置**：确保服务器端口正确且未被占用
3. **消息格式**：调试指令必须严格按照 `GETV[变量名]` 和 `SETV[变量名,变量值]` 格式发送
4. **变量类型**：SETV 功能块支持多种数据类型，但输入必须是字符串格式
5. **错误处理**：当前模板未包含详细的错误处理逻辑，实际应用中应添加错误处理
6. **安全性**：调试功能应在生产环境中适当限制，避免安全风险
7. **重连机制**：当连接断开时，TCP_CLIENT 功能块会自动尝试重新连接，确保通信的可靠性

## 9. 故障排除

### 9.1 连接失败

- 检查网络连接是否正常
- 验证服务器地址和端口是否正确
- 确认服务器是否正在运行并监听指定端口

### 9.2 指令解析失败

- 检查指令格式是否正确
- 验证变量名是否存在
- 确认消息模板是否正确配置

### 9.3 升级失败

- 检查升级服务器地址是否正确
- 确认服务器上是否有对应的固件文件
- 验证网络连接是否稳定

## 10. 总结

template.st 是一个功能完整的 ST 程序框架，提供了以下核心功能：

1. **TCP 通信**：实现与调试服务器的连接和数据交换，支持自动重连
2. **调试指令处理**：支持 GETV 和 SETV 指令，用于远程变量读写
3. **OTA 升级**：支持 PLC 程序和 ESP 固件的远程升级
4. **系统信息管理**：提供设备信息的配置和获取

该模板可作为 AI 自动生成 ST 程序的基础框架，通过扩展和定制，可以适应各种 IoT 应用场景。开发者可以根据具体需求，修改配置参数、添加控制逻辑、集成其他通信协议，构建完整的工业物联网解决方案。