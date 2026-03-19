# TON 功能块使用经验总结

## 1. TON 功能块简介

TON（Timer On Delay）是 IEC 61131-3 标准中的通电延时定时器功能块，用于实现延时启动、延时触发等功能。它是工业自动化控制中最常用的定时器功能块之一。

### 1.1 基本功能

- **功能**：当输入信号 IN 为 TRUE 时，经过设定的延时时间 PT 后，输出 Q 变为 TRUE
- **复位**：当输入信号 IN 变为 FALSE 时，输出 Q 立即变为 FALSE，定时器复位
- **计时**：定时器会实时更新已用时间 ET，可用于监控计时过程

## 2. TON 功能块参数

| 参数 | 类型 | 方向 | 描述 |
|------|------|------|------|
| EN | BOOL | 输入 | 使能信号，为 TRUE 时功能块正常工作 |
| ENO | BOOL | 输出 | 使能输出，当 EN 为 TRUE 且功能块正常工作时为 TRUE |
| IN | BOOL | 输入 | 触发信号，为 TRUE 时开始计时 |
| PT | TIME | 输入 | 延时时间，设定的延时值 |
| Q | BOOL | 输出 | 输出信号，延时结束后变为 TRUE |
| ET | TIME | 输出 | 已用时间，实时显示当前计时值 |

## 3. TON 功能块工作原理

1. **初始状态**：IN 为 FALSE，Q 为 FALSE，ET 为 T#0ms
2. **开始计时**：当 IN 从 FALSE 变为 TRUE 时，定时器开始计时，ET 逐渐增加
3. **延时结束**：当 ET >= PT 时，Q 变为 TRUE
4. **保持状态**：IN 保持 TRUE，Q 保持 TRUE，ET 保持为 PT
5. **复位**：当 IN 变为 FALSE 时，Q 立即变为 FALSE，ET 复位为 T#0ms

### 3.1 时序变化表格

#### 场景 1：输入为 TRUE 的时间大于等于 PT（PT = T#500ms）

| 时间点 | IN 状态 | Q 状态 | ET 值    | 说明                   |
|--------|---------|--------|----------|------------------------|
| t0     | FALSE   | FALSE  | T#0ms    | 初始状态               |
| t1     | TRUE    | FALSE  | T#0ms    | IN 变为 TRUE，开始计时 |
| t2     | TRUE    | FALSE  | T#200ms  | 计时中，ET 逐渐增加    |
| t3     | TRUE    | FALSE  | T#499ms  | 接近延时结束           |
| t4     | TRUE    | TRUE   | T#500ms  | ET >= PT，Q 变为 TRUE  |
| t5     | TRUE    | TRUE   | T#500ms  | IN 保持 TRUE，Q 保持 TRUE |
| t6     | FALSE   | FALSE  | T#0ms    | IN 变为 FALSE，Q 立即复位 |

#### 场景 2：输入为 TRUE 的时间小于 PT（PT = T#500ms，输入为 TRUE 的时间 = T#200ms）

| 时间点 | IN 状态 | Q 状态 | ET 值    | 说明                   |
|--------|---------|--------|----------|------------------------|
| t0     | FALSE   | FALSE  | T#0ms    | 初始状态               |
| t1     | TRUE    | FALSE  | T#0ms    | IN 变为 TRUE，开始计时 |
| t2     | TRUE    | FALSE  | T#199ms  | 计时中，ET 逐渐增加    |
| t3     | FALSE   | FALSE  | T#0ms    | IN 变为 FALSE，Q 立即复位 |
| t4     | FALSE   | FALSE  | T#0ms    | 保持状态               |
| t5     | TRUE    | FALSE  | T#0ms    | IN 再次变为 TRUE，重新开始计时 |
| t6     | TRUE    | FALSE  | T#499ms  | 计时中，ET 逐渐增加    |
| t7     | TRUE    | TRUE   | T#500ms  | ET >= PT，Q 变为 TRUE  |
| t8     | FALSE   | FALSE  | T#0ms    | IN 变为 FALSE，Q 立即复位 |

**注**：表格展示了 TON 功能块在不同输入条件下的工作周期。

## 4. TON 功能块使用示例

### 4.1 基本延时启动

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

**说明**：当 StartSignal 为 TRUE 时，经过 5 秒延时后，MotorEnabled 变为 TRUE，实现电机的延时启动。

### 4.2 脉冲间隔测量

```st
// 使用 TON 测量脉冲间隔
VAR
    TON0: TON;
    TON1: TON;
    PULSE_PERIOD_TIME: TIME := T#500ms;
    M: BOOL := FALSE;
    TM: TIME;
    PTM: TIME;
END_VAR

TON0(IN:=NOT TON0.Q, PT:=PULSE_PERIOD_TIME);
TON1(IN:=NOT TON0.Q, PT:=T#20s);
IF TON0.Q = FALSE THEN
    TM := TON1.ET;
ELSIF M = FALSE THEN
    M := TRUE;
ELSE
    PTM := TM;
END_IF;
```

**说明**：使用 TON0 实现自振荡电路生成脉冲，使用 TON1 测量脉冲间隔时间，最终将测量结果存储在 PTM 变量中。

### 4.3 故障检测延时

```st
// 使用 TON 实现故障检测延时
VAR
    FaultSignal: BOOL;
    FaultTimer: TON;
    FaultAlarm: BOOL;
END_VAR

FaultTimer(IN:=FaultSignal, PT:=T#3s);
FaultAlarm := FaultTimer.Q;
```

**说明**：当 FaultSignal 持续为 TRUE 超过 3 秒时，FaultAlarm 变为 TRUE，实现故障的延时报警，避免误报警。

### 4.4 循环定时控制

```st
// 使用 TON 实现循环定时控制
VAR
    Timer: TON;
    CycleFlag: BOOL := FALSE;
END_VAR

Timer(IN:=NOT CycleFlag, PT:=T#10s);
IF Timer.Q THEN
    // 执行循环任务
    // ...
    CycleFlag := TRUE;  // 触发定时器复位
ELSIF NOT Timer.Q AND CycleFlag THEN
    CycleFlag := FALSE;  // 允许定时器重新开始计时
END_IF;
```

**说明**：每 10 秒执行一次循环任务。当定时器计时完成（Timer.Q为TRUE）时，执行循环任务并设置CycleFlag为TRUE，使定时器复位。当定时器复位后（Timer.Q为FALSE）且CycleFlag为TRUE时，将CycleFlag设置为FALSE，允许定时器重新开始计时，从而实现循环定时控制。

### 4.5 输入信号防抖

```st
// 使用 TON 实现输入信号防抖
VAR
    RawInput: BOOL;          // 原始输入信号
    DebouncedInput: BOOL;    // 防抖后的输入信号
    DebounceTimer: TON;      // 防抖定时器
END_VAR

// 当原始输入信号变化时，启动防抖定时器
DebounceTimer(IN:=RawInput, PT:=T#50ms);

// 当定时器计时完成后，才认为输入信号稳定
DebouncedInput := DebounceTimer.Q;
```

**说明**：当 RawInput 信号发生变化时，需要保持稳定 50ms 后，DebouncedInput 才会反映 RawInput 的状态，从而实现输入信号的防抖，避免因信号抖动导致的误触发。

## 5. TON 功能块使用注意事项

### 5.1 时间单位格式

- TIME 类型的参数格式为 `T#d hh:mm:ss.ms`，例如：
  - `T#1s` - 1秒
  - `T#500ms` - 500毫秒
  - `T#1m30s` - 1分30秒
  - `T#0h0m10s` - 10秒

### 5.2 初始化

- 每个功能块都有对应的初始化函数（如 `TON_init__`），在使用功能块前应调用初始化函数
- 初始化函数会将功能块的内部状态变量重置为初始值

### 5.3 使能信号

- EN 参数用于功能块的级联控制，当 EN 为 FALSE 时，功能块不工作
- ENO 参数用于指示功能块是否正常工作，可用于级联到下一个功能块

### 5.4 精度考虑

- 定时器的精度取决于 PLC 的扫描周期
- 对于高精度定时，应选择扫描周期较小的任务
- 避免在扫描周期较长的任务中使用高精度定时器

### 5.5 内存使用

- 每个 TON 功能块实例会占用一定的内存空间
- 在资源受限的系统中，应合理使用定时器，避免过多实例

## 6. TON 功能块常见问题及解决方案

### 6.1 定时器不启动

**问题**：输入信号 IN 为 TRUE，但定时器不计时

**解决方案**：
- 检查 EN 参数是否为 TRUE
- 检查 PT 参数是否设置正确
- 检查功能块是否正确初始化

### 6.2 定时器不复位

**问题**：输入信号 IN 为 FALSE，但定时器不复位

**解决方案**：
- 检查 IN 参数是否确实变为 FALSE
- 检查功能块是否被其他逻辑强制保持

### 6.3 定时精度不够

**问题**：实际延时时间与设定值偏差较大

**解决方案**：
- 减小 PLC 的扫描周期
- 使用更高精度的定时器功能块
- 考虑使用硬件定时器

### 6.4 定时器冲突

**问题**：多个定时器同时使用时出现冲突

**解决方案**：
- 为每个定时器分配独立的变量
- 避免在同一扫描周期内多次触发同一定时器
- 合理安排定时器的执行顺序

## 7. TON 功能块与其他定时器的比较

| 定时器类型 | 功能 | 适用场景 |
|-----------|------|----------|
| TON | 通电延时 | 延时启动、故障检测 |
| TOF | 断电延时 | 延时停止、保持输出 |
| TP | 脉冲定时器 | 生成固定宽度的脉冲 |

## 8. 最佳实践

### 8.1 命名规范

- 使用有意义的变量名，如 `MotorStartTimer`、`FaultDetectionTimer`
- 为定时器参数添加注释，说明延时时间的含义

### 8.2 模块化设计

- 将定时器逻辑封装到功能块中，提高代码复用性
- 使用结构化编程，将定时器相关逻辑组织到专门的程序块中

### 8.3 错误处理

- 添加定时器故障检测逻辑，如定时器超时检测
- 为关键定时器添加监控和报警机制

### 8.4 性能优化

- 对于长时间延时，考虑使用计数器替代定时器，减少 CPU 负担
- 合理设置定时器的扫描周期，平衡精度和性能

## 9. 总结

TON 功能块是工业自动化控制中常用的延时控制工具，通过合理使用 TON 功能块，可以实现各种延时控制逻辑，如延时启动、故障检测、循环控制等。

在使用 TON 功能块时，应注意以下几点：

1. **正确设置参数**：根据实际需求设置合适的 PT 值和输入信号
2. **合理初始化**：在使用前正确初始化功能块
3. **注意精度**：根据应用场景选择合适的扫描周期
4. **避免冲突**：为每个定时器分配独立的变量和资源
5. **优化设计**：采用模块化设计，提高代码可维护性

通过掌握 TON 功能块的使用方法和最佳实践，可以更高效地实现各种延时控制逻辑，提高控制系统的可靠性和稳定性。