# IEC 61131-3 标准功能块库说明文档

## 1. 概述

`iec_std_FB.h` 文件是 IEC 61131-3 标准功能块的 C 语言实现，包含了工业自动化领域常用的标准功能块。这些功能块按照 IEC 61131-3 标准定义，为 PLC 程序提供了基础的控制逻辑功能。

### 1.1 文件来源

该文件由 `iec2c`（matiec C 编译器）生成，使用 `lib` 目录中的 `*.txt` 文件作为源文件。文件中包含了以下手动修改：
- 将生成的 .h 和 .c 文件合并为单个文件
- 移除函数的前向声明
- 将函数原型改为 `static`

### 1.2 文件版本

文件有两个版本：
- `iec_std_FB.h`：当所有函数和功能块的 EN 和 ENO 参数被隐式生成时使用
- `iec_std_FB_no_ENENO.h`：当所有函数和功能块的 EN 和 ENO 参数不被隐式生成时使用

## 2. 功能块分类

根据 IEC 61131-3 标准，功能块分为以下几类：

### 2.1 触发器功能块
- **R_TRIG**：上升沿触发器
- **F_TRIG**：下降沿触发器

### 2.2 逻辑功能块
- **SR**：置位优先锁存器
- **RS**：复位优先锁存器

### 2.3 计数器功能块
- **CTU**：增计数器（INT类型）
- **CTU_DINT**：增计数器（DINT类型）
- **CTU_LINT**：增计数器（LINT类型）
- **CTU_UDINT**：增计数器（UDINT类型）
- **CTU_ULINT**：增计数器（ULINT类型）
- **CTD**：减计数器（INT类型）
- **CTD_DINT**：减计数器（DINT类型）
- **CTD_LINT**：减计数器（LINT类型）
- **CTD_UDINT**：减计数器（UDINT类型）
- **CTD_ULINT**：减计数器（ULINT类型）
- **CTUD**：增减计数器（INT类型）
- **CTUD_DINT**：增减计数器（DINT类型）
- **CTUD_LINT**：增减计数器（LINT类型）
- **CTUD_UDINT**：增减计数器（UDINT类型）
- **CTUD_ULINT**：增减计数器（ULINT类型）

### 2.4 定时器功能块
- **TP**：脉冲定时器
- **TON**：通电延时定时器
- **TOF**：断电延时定时器

### 2.5 控制功能块
- **DERIVATIVE**：微分器
- **HYSTERESIS**：迟滞比较器
- **INTEGRAL**：积分器
- **PID**：比例积分微分控制器
- **PIDLMT**：带限幅的PID控制器
- **RAMP**：斜坡函数发生器
- **SEMA**：信号量

## 3. 功能块详细说明

### 3.1 触发器功能块

#### 3.1.1 R_TRIG（上升沿触发器）

**功能**：检测输入信号的上升沿，当输入信号从 FALSE 变为 TRUE 时，输出一个脉冲。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **CLK**（输入，BOOL）：时钟信号
- **Q**（输出，BOOL）：输出信号

**内部变量**：
- **M**：记忆变量，用于存储上一个周期的 CLK 值

**工作原理**：当 CLK 从 FALSE 变为 TRUE 时，Q 输出 TRUE 一个扫描周期。

#### 3.1.2 F_TRIG（下降沿触发器）

**功能**：检测输入信号的下降沿，当输入信号从 TRUE 变为 FALSE 时，输出一个脉冲。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **CLK**（输入，BOOL）：时钟信号
- **Q**（输出，BOOL）：输出信号

**内部变量**：
- **M**：记忆变量，用于存储上一个周期的 CLK 值

**工作原理**：当 CLK 从 TRUE 变为 FALSE 时，Q 输出 TRUE 一个扫描周期。

### 3.2 逻辑功能块

#### 3.2.1 SR（置位优先锁存器）

**功能**：置位优先的锁存器，当 S1 为 TRUE 时，Q1 置位；当 R 为 TRUE 时，Q1 复位。当 S1 和 R 同时为 TRUE 时，S1 优先。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **S1**（输入，BOOL）：置位信号
- **R**（输入，BOOL）：复位信号
- **Q1**（输出，BOOL）：输出信号

**工作原理**：
- 当 S1 为 TRUE 时，Q1 置为 TRUE
- 当 R 为 TRUE 且 S1 为 FALSE 时，Q1 置为 FALSE
- 当 S1 和 R 同时为 TRUE 时，Q1 置为 TRUE

#### 3.2.2 RS（复位优先锁存器）

**功能**：复位优先的锁存器，当 S 为 TRUE 时，Q1 置位；当 R1 为 TRUE 时，Q1 复位。当 S 和 R1 同时为 TRUE 时，R1 优先。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **S**（输入，BOOL）：置位信号
- **R1**（输入，BOOL）：复位信号
- **Q1**（输出，BOOL）：输出信号

**工作原理**：
- 当 S 为 TRUE 且 R1 为 FALSE 时，Q1 置为 TRUE
- 当 R1 为 TRUE 时，Q1 置为 FALSE
- 当 S 和 R1 同时为 TRUE 时，Q1 置为 FALSE

### 3.3 计数器功能块

#### 3.3.1 CTU（增计数器）

**功能**：当 CU 输入信号出现上升沿时，计数器值增加 1，当计数器值达到预设值 PV 时，输出 Q 变为 TRUE。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **CU**（输入，BOOL）：计数输入
- **R**（输入，BOOL）：复位信号
- **PV**（输入，INT）：预设值
- **Q**（输出，BOOL）：计数达到预设值时输出 TRUE
- **CV**（输出，INT）：当前计数值

**内部变量**：
- **CU_T**：上升沿触发器，用于检测 CU 的上升沿

**工作原理**：
- 当 R 为 TRUE 时，CV 复位为 0
- 当 CU 出现上升沿且 CV < PV 时，CV 增加 1
- 当 CV >= PV 时，Q 为 TRUE

#### 3.3.2 CTD（减计数器）

**功能**：当 CD 输入信号出现上升沿时，计数器值减少 1，当计数器值减到 0 时，输出 Q 变为 TRUE。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **CD**（输入，BOOL）：计数输入
- **LD**（输入，BOOL）：加载信号，将 PV 值加载到 CV
- **PV**（输入，INT）：预设值
- **Q**（输出，BOOL）：计数减到 0 时输出 TRUE
- **CV**（输出，INT）：当前计数值

**内部变量**：
- **CD_T**：上升沿触发器，用于检测 CD 的上升沿

**工作原理**：
- 当 LD 为 TRUE 时，CV 加载为 PV
- 当 CD 出现上升沿且 CV > 0 时，CV 减少 1
- 当 CV <= 0 时，Q 为 TRUE

#### 3.3.3 CTUD（增减计数器）

**功能**：结合了 CTU 和 CTD 的功能，可同时进行递增和递减计数。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **CU**（输入，BOOL）：递增计数输入
- **CD**（输入，BOOL）：递减计数输入
- **R**（输入，BOOL）：复位信号
- **LD**（输入，BOOL）：加载信号，将 PV 值加载到 CV
- **PV**（输入，INT）：预设值
- **QU**（输出，BOOL）：递增计数达到预设值时输出 TRUE
- **QD**（输出，BOOL）：递减计数到 0 时输出 TRUE
- **CV**（输出，INT）：当前计数值

**内部变量**：
- **CU_T**：上升沿触发器，用于检测 CU 的上升沿
- **CD_T**：上升沿触发器，用于检测 CD 的上升沿

**工作原理**：
- 当 R 为 TRUE 时，CV 复位为 0
- 当 LD 为 TRUE 时，CV 加载为 PV
- 当 CU 出现上升沿且 CV < PV 时，CV 增加 1
- 当 CD 出现上升沿且 CV > 0 时，CV 减少 1
- 当 CV >= PV 时，QU 为 TRUE
- 当 CV <= 0 时，QD 为 TRUE

### 3.4 定时器功能块

#### 3.4.1 TP（脉冲定时器）

**功能**：当输入 IN 为 TRUE 时，输出 Q 变为 TRUE 并保持 PT 时间，然后变为 FALSE。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **IN**（输入，BOOL）：输入信号
- **PT**（输入，TIME）：脉冲时间
- **Q**（输出，BOOL）：输出信号
- **ET**（输出，TIME）：已用时间

**内部变量**：
- **STATE**：状态变量
- **PREV_IN**：上一个周期的 IN 值
- **CURRENT_TIME**：当前时间
- **START_TIME**：开始时间

**工作原理**：
- 当 IN 从 FALSE 变为 TRUE 时，Q 变为 TRUE，记录开始时间
- 当经过 PT 时间后，Q 变为 FALSE
- 当 IN 变为 FALSE 且定时器已触发后，定时器复位

#### 3.4.2 TON（通电延时定时器）

**功能**：当输入 IN 为 TRUE 时，经过 PT 时间后，输出 Q 变为 TRUE。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **IN**（输入，BOOL）：输入信号
- **PT**（输入，TIME）：延时时间
- **Q**（输出，BOOL）：输出信号
- **ET**（输出，TIME）：已用时间

**内部变量**：
- **STATE**：状态变量
- **PREV_IN**：上一个周期的 IN 值
- **CURRENT_TIME**：当前时间
- **START_TIME**：开始时间

**工作原理**：
- 当 IN 从 FALSE 变为 TRUE 时，开始计时
- 当经过 PT 时间后，Q 变为 TRUE
- 当 IN 变为 FALSE 时，Q 立即变为 FALSE，定时器复位

#### 3.4.3 TOF（断电延时定时器）

**功能**：当输入 IN 从 TRUE 变为 FALSE 时，输出 Q 保持 TRUE 并持续 PT 时间，然后变为 FALSE。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **IN**（输入，BOOL）：输入信号
- **PT**（输入，TIME）：延时时间
- **Q**（输出，BOOL）：输出信号
- **ET**（输出，TIME）：已用时间

**内部变量**：
- **STATE**：状态变量
- **PREV_IN**：上一个周期的 IN 值
- **CURRENT_TIME**：当前时间
- **START_TIME**：开始时间

**工作原理**：
- 当 IN 为 TRUE 时，Q 为 TRUE
- 当 IN 从 TRUE 变为 FALSE 时，开始计时，Q 保持 TRUE
- 当经过 PT 时间后，Q 变为 FALSE
- 当 IN 再次变为 TRUE 时，定时器复位，Q 立即变为 TRUE

### 3.5 控制功能块

#### 3.5.1 DERIVATIVE（微分器）

**功能**：计算输入信号的微分（变化率）。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **RUN**（输入，BOOL）：运行信号
- **XIN**（输入，REAL）：输入信号
- **CYCLE**（输入，TIME）：采样周期
- **XOUT**（输出，REAL）：微分输出

**内部变量**：
- **X1, X2, X3**：历史输入值

**工作原理**：
- 当 RUN 为 TRUE 时，计算输入信号的微分
- 当 RUN 为 FALSE 时，输出为 0，并初始化历史值

#### 3.5.2 HYSTERESIS（迟滞比较器）

**功能**：带有迟滞的比较器，用于避免在阈值附近的振荡。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **XIN1**（输入，REAL）：输入信号
- **XIN2**（输入，REAL）：参考值
- **EPSx**（输入，REAL）：迟滞值
- **Q**（输出，BOOL）：比较结果

**工作原理**：
- 当 XIN1 > XIN2 + EPSx 时，Q 为 TRUE
- 当 XIN1 < XIN2 - EPSx 时，Q 为 FALSE
- 当 XIN2 - EPSx <= XIN1 <= XIN2 + EPSx 时，Q 保持之前的状态

#### 3.5.3 INTEGRAL（积分器）

**功能**：计算输入信号的积分。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **RUN**（输入，BOOL）：运行信号
- **R1**（输入，BOOL）：复位信号
- **XIN**（输入，REAL）：输入信号
- **X0**（输入，REAL）：初始值
- **CYCLE**（输入，TIME）：采样周期
- **Q**（输出，BOOL）：使能输出
- **XOUT**（输出，REAL）：积分输出

**工作原理**：
- 当 R1 为 TRUE 时，XOUT 复位为 X0
- 当 RUN 为 TRUE 时，计算输入信号的积分

#### 3.5.4 PID（比例积分微分控制器）

**功能**：实现比例积分微分控制算法。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **AUTO**（输入，BOOL）：自动模式信号
- **PV**（输入，REAL）：过程变量
- **SP**（输入，REAL）：设定值
- **X0**（输入，REAL）：初始输出值
- **KP**（输入，REAL）：比例增益
- **TR**（输入，REAL）：积分时间
- **TD**（输入，REAL）：微分时间
- **CYCLE**（输入，TIME）：控制周期
- **XOUT**（输出，REAL）：控制输出

**内部变量**：
- **ERROR**：误差值
- **ITERM**：积分器实例
- **DTERM**：微分器实例

**工作原理**：
- 计算误差值：ERROR = PV - SP
- 当 AUTO 为 TRUE 时，使用 PID 算法计算输出
- 当 AUTO 为 FALSE 时，输出保持为 X0

#### 3.5.5 PIDLMT（带限幅的PID控制器）

**功能**：带有输出限幅的 PID 控制器。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **AUTO**（输入，BOOL）：自动模式信号
- **PV**（输入，REAL）：过程变量
- **SP**（输入，REAL）：设定值
- **X0**（输入，REAL）：初始输出值
- **KP**（输入，REAL）：比例增益
- **TR**（输入，REAL）：积分时间
- **TD**（输入，REAL）：微分时间
- **CYCLE**（输入，TIME）：控制周期
- **MX**（输入，REAL）：输出上限
- **MN**（输入，REAL）：输出下限
- **XOUT**（输出，REAL）：控制输出

**内部变量**：
- **ERROR**：误差值
- **ITERM**：积分器实例
- **DTERM**：微分器实例

**工作原理**：
- 与 PID 控制器相同，但增加了输出限幅功能
- 当计算输出超过 MX 时，输出 MX
- 当计算输出低于 MN 时，输出 MN

#### 3.5.6 RAMP（斜坡函数发生器）

**功能**：生成从 X0 到 X1 的线性斜坡信号。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **RUN**（输入，BOOL）：运行信号
- **X0**（输入，REAL）：起始值
- **X1**（输入，REAL）：目标值
- **TR**（输入，TIME）：斜坡时间
- **CYCLE**（输入，TIME）：采样周期
- **BUSY**（输出，BOOL）：忙信号
- **XOUT**（输出，REAL）：斜坡输出

**内部变量**：
- **XI**：当前起始值
- **T**：已用时间

**工作原理**：
- 当 RUN 为 TRUE 时，开始生成斜坡信号
- 当经过 TR 时间后，输出达到 X1，BUSY 变为 FALSE
- 当 RUN 为 FALSE 时，输出立即变为 X0，定时器复位

#### 3.5.7 SEMA（信号量）

**功能**：实现信号量功能，用于资源分配和互斥访问。

**参数**：
- **EN**（输入，BOOL）：使能信号
- **ENO**（输出，BOOL）：使能输出
- **CLAIM**（输入，BOOL）：请求信号
- **RELEASE**（输入，BOOL）：释放信号
- **BUSY**（输出，BOOL）：忙信号

**内部变量**：
- **Q_INTERNAL**：内部状态变量

**工作原理**：
- 当 CLAIM 为 TRUE 时，BUSY 变为 TRUE
- 当 RELEASE 为 TRUE 时，BUSY 变为 FALSE
- 当 CLAIM 和 RELEASE 同时为 TRUE 时，BUSY 保持 TRUE

## 4. 与 IEC 61131-3 标准的对应关系

| 功能块名称 | IEC 61131-3 标准对应 | 功能描述 |
|-----------|-------------------|----------|
| R_TRIG | 标准上升沿触发器 | 检测输入信号的上升沿 |
| F_TRIG | 标准下降沿触发器 | 检测输入信号的下降沿 |
| SR | 标准置位优先锁存器 | 置位优先的逻辑锁存 |
| RS | 标准复位优先锁存器 | 复位优先的逻辑锁存 |
| CTU | 标准增计数器 | 递增计数功能 |
| CTD | 标准减计数器 | 递减计数功能 |
| CTUD | 标准增减计数器 | 递增和递减计数功能 |
| TP | 标准脉冲定时器 | 生成指定时间的脉冲 |
| TON | 标准通电延时定时器 | 通电后延时输出 |
| TOF | 标准断电延时定时器 | 断电后延时输出 |
| DERIVATIVE | 标准微分器 | 计算输入信号的微分 |
| HYSTERESIS | 标准迟滞比较器 | 带迟滞的信号比较 |
| INTEGRAL | 标准积分器 | 计算输入信号的积分 |
| PID | 标准PID控制器 | 比例积分微分控制 |
| PIDLMT | 带限幅的PID控制器 | 带输出限幅的PID控制 |
| RAMP | 标准斜坡函数发生器 | 生成线性斜坡信号 |
| SEMA | 标准信号量 | 资源分配和互斥访问 |

## 5. 使用示例

### 5.1 触发器示例

```st
// 使用 R_TRIG 检测按钮按下
VAR
    Button: BOOL;
    ButtonPressed: BOOL;
    Trig: R_TRIG;
END_VAR

Trig(CLK:=Button);
ButtonPressed := Trig.Q;
```

### 5.2 计数器示例

```st
// 使用 CTU 计数产品数量
VAR
    ProductDetected: BOOL;
    ResetCounter: BOOL;
    Counter: CTU;
    TotalProducts: INT;
    CountReached: BOOL;
END_VAR

Counter(CU:=ProductDetected, R:=ResetCounter, PV:=100);
TotalProducts := Counter.CV;
CountReached := Counter.Q;
```

### 5.3 定时器示例

```st
// 使用 TON 实现延时启动
VAR
    StartSignal: BOOL;
    Timer: TON;
    MotorEnabled: BOOL;
END_VAR

Timer(IN:=StartSignal, PT:=T#5s);
MotorEnabled := Timer.Q;
```

### 5.4 PID 控制器示例

```st
// 使用 PID 控制温度
VAR
    Temperature: REAL;
    Setpoint: REAL := 25.0;
    PID_Controller: PID;
    HeaterOutput: REAL;
END_VAR

PID_Controller(AUTO:=TRUE, PV:=Temperature, SP:=Setpoint, 
              KP:=1.0, TR:=10.0, TD:=2.0, CYCLE:=T#100ms);
HeaterOutput := PID_Controller.XOUT;
```

## 6. 注意事项

1. **EN/ENO 参数**：所有功能块都包含 EN（使能输入）和 ENO（使能输出）参数，用于功能块的级联控制。

2. **数据类型**：计数器功能块有多种数据类型版本（INT、DINT、LINT、UDINT、ULINT），可根据实际需求选择合适的类型。

3. **初始化**：每个功能块都有对应的初始化函数（如 `R_TRIG_init__`），在使用功能块前应调用初始化函数。

4. **时间单位**：时间相关参数（如 PT、CYCLE、TR）使用 TIME 类型，格式为 T#d hh:mm:ss.ms。

5. **内存使用**：功能块实例会占用一定的内存空间，在资源受限的系统中应注意合理使用。

## 7. 总结

`iec_std_FB.h` 文件实现了 IEC 61131-3 标准中定义的常用功能块，为 PLC 程序提供了基础的控制逻辑功能。这些功能块按照标准定义实现，可用于各种工业自动化控制场景。

通过使用这些标准化的功能块，开发者可以更快速、更可靠地开发 PLC 程序，提高代码的可移植性和可维护性。同时，这些功能块的 C 语言实现也使得它们可以在不同的硬件平台上运行，为跨平台开发提供了便利。