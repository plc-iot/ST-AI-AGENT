# TOF 功能块使用经验总结

## 1. TOF 功能块简介

TOF（Timer Off Delay）是 IEC 61131-3 标准中的断电延时定时器功能块，用于实现延时停止、保持输出等功能。它是工业自动化控制中常用的定时器功能块之一，特别适用于需要在输入信号断开后保持输出一段时间的场景。

### 1.1 基本功能

- **功能**：当输入信号 IN 从 TRUE 变为 FALSE 时，输出 Q 保持 TRUE 并持续 PT 时间，然后变为 FALSE
- **特性**：在输入信号 IN 为 TRUE 时，输出 Q 立即为 TRUE；当 IN 变为 FALSE 时，开始延时，延时结束后 Q 变为 FALSE
- **复位**：当输入信号 IN 再次变为 TRUE 时，定时器复位，Q 立即变为 TRUE
- **计时**：定时器会实时更新已用时间 ET，可用于监控计时过程

## 2. TOF 功能块参数

| 参数 | 类型 | 方向 | 描述 |
|------|------|------|------|
| EN | BOOL | 输入 | 使能信号，为 TRUE 时功能块正常工作 |
| ENO | BOOL | 输出 | 使能输出，当 EN 为 TRUE 且功能块正常工作时为 TRUE |
| IN | BOOL | 输入 | 输入信号，控制定时器的状态 |
| PT | TIME | 输入 | 延时时间，设定的延时值 |
| Q | BOOL | 输出 | 输出信号，延时期间为 TRUE |
| ET | TIME | 输出 | 已用时间，实时显示当前计时值 |

## 3. TOF 功能块工作原理

1. **初始状态**：IN 为 FALSE，Q 为 FALSE，ET 为 T#0ms
2. **输入为 TRUE**：当 IN 变为 TRUE 时，Q 立即变为 TRUE，ET 复位为 T#0ms
3. **保持状态**：IN 保持 TRUE，Q 保持 TRUE，ET 保持为 T#0ms
4. **开始延时**：当 IN 从 TRUE 变为 FALSE 时，开始计时，ET 逐渐增加，Q 保持 TRUE
5. **延时结束**：当 ET >= PT 时，Q 变为 FALSE，ET 保持为 PT
6. **复位**：当 IN 再次变为 TRUE 时，Q 立即变为 TRUE，ET 复位为 T#0ms

### 3.1 时序变化表格

#### 场景 1：正常断电延时（PT = T#500ms）

| 时间点 | IN 状态 | Q 状态 | ET 值    | 说明                   |
|--------|---------|--------|----------|------------------------|
| t0     | FALSE   | FALSE  | T#0ms    | 初始状态               |
| t1     | TRUE    | TRUE   | T#0ms    | IN 变为 TRUE，Q 立即变为 TRUE |
| t2     | TRUE    | TRUE   | T#0ms    | IN 保持 TRUE，Q 保持 TRUE |
| t3     | FALSE   | TRUE   | T#0ms    | IN 变为 FALSE，开始计时 |
| t4     | FALSE   | TRUE   | T#200ms  | 计时中，ET 逐渐增加    |
| t5     | FALSE   | TRUE   | T#499ms  | 接近延时结束           |
| t6     | FALSE   | FALSE  | T#500ms  | ET >= PT，Q 变为 FALSE |
| t7     | FALSE   | FALSE  | T#500ms  | 保持状态               |

#### 场景 2：延时期间输入重新变为 TRUE（PT = T#500ms）

| 时间点 | IN 状态 | Q 状态 | ET 值    | 说明                   |
|--------|---------|--------|----------|------------------------|
| t0     | FALSE   | FALSE  | T#0ms    | 初始状态               |
| t1     | TRUE    | TRUE   | T#0ms    | IN 变为 TRUE，Q 立即变为 TRUE |
| t2     | FALSE   | TRUE   | T#0ms    | IN 变为 FALSE，开始计时 |
| t3     | FALSE   | TRUE   | T#200ms  | 计时中，ET 逐渐增加    |
| t4     | TRUE    | TRUE   | T#0ms    | IN 再次变为 TRUE，定时器复位 |
| t5     | TRUE    | TRUE   | T#0ms    | IN 保持 TRUE，Q 保持 TRUE |
| t6     | FALSE   | TRUE   | T#0ms    | IN 变为 FALSE，重新开始计时 |
| t7     | FALSE   | TRUE   | T#499ms  | 计时中，ET 逐渐增加    |
| t8     | FALSE   | FALSE  | T#500ms  | ET >= PT，Q 变为 FALSE |

**注**：表格展示了 TOF 功能块在不同场景下的工作周期。

## 4. TOF 功能块使用示例

### 4.1 基本断电延时

```st
// 使用 TOF 实现断电延时
VAR
    InputSignal: BOOL;
    OffDelayTimer: TOF;
    OutputSignal: BOOL;
END_VAR

OffDelayTimer(IN:=InputSignal, PT:=T#2s);
OutputSignal := OffDelayTimer.Q;
```

**说明**：当 InputSignal 从 TRUE 变为 FALSE 时，OutputSignal 会保持 TRUE 2 秒，然后变为 FALSE，实现断电延时功能。

### 4.2 设备停机冷却

```st
// 使用 TOF 实现设备停机后的冷却
VAR
    MotorRunning: BOOL;
    CoolDownTimer: TOF;
    CoolerOn: BOOL;
END_VAR

CoolDownTimer(IN:=MotorRunning, PT:=T#5min);
CoolerOn := CoolDownTimer.Q;
```

**说明**：当电机停止运行（MotorRunning 变为 FALSE）时，冷却器会继续运行 5 分钟，确保设备充分冷却。

### 4.3 报警信号保持

```st
// 使用 TOF 实现报警信号保持
VAR
    AlarmTrigger: BOOL;
    AlarmTimer: TOF;
    AlarmActive: BOOL;
END_VAR

AlarmTimer(IN:=AlarmTrigger, PT:=T#30s);
AlarmActive := AlarmTimer.Q;
```

**说明**：当报警触发信号（AlarmTrigger）变为 FALSE 后，报警信号（AlarmActive）会保持 30 秒，确保操作人员有足够的时间注意到报警。

### 4.4 系统断电应急处理

```st
// 使用 TOF 实现系统断电后的应急处理
VAR
    PowerOn: BOOL;
    EmergencyTimer: TOF;
    EmergencyPower: BOOL;
END_VAR

EmergencyTimer(IN:=PowerOn, PT:=T#10s);
EmergencyPower := EmergencyTimer.Q;
```

**说明**：当系统断电（PowerOn 变为 FALSE）时，应急电源会保持供电 10 秒，为系统提供足够的时间进行安全关闭操作。

## 5. TOF 功能块使用注意事项

### 5.1 时间单位格式

- TIME 类型的参数格式为 `T#d hh:mm:ss.ms`，例如：
  - `T#1s` - 1秒
  - `T#500ms` - 500毫秒
  - `T#1m30s` - 1分30秒
  - `T#0h0m10s` - 10秒

### 5.2 初始化

- 每个功能块都有对应的初始化函数（如 `TOF_init__`），在使用功能块前应调用初始化函数
- 初始化函数会将功能块的内部状态变量重置为初始值

### 5.3 使能信号

- EN 参数用于功能块的级联控制，当 EN 为 FALSE 时，功能块不工作
- ENO 参数用于指示功能块是否正常工作，可用于级联到下一个功能块

### 5.4 精度考虑

- 定时器的精度取决于 PLC 的扫描周期
- 对于高精度定时，应选择扫描周期较小的任务
- 避免在扫描周期较长的任务中使用高精度定时器

### 5.5 内存使用

- 每个 TOF 功能块实例会占用一定的内存空间
- 在资源受限的系统中，应合理使用定时器，避免过多实例

### 5.6 输入信号处理

- TOF 功能块对输入信号的下降沿敏感，当 IN 从 TRUE 变为 FALSE 时开始计时
- 在延时期间，如果 IN 再次变为 TRUE，定时器会复位，Q 立即变为 TRUE
- 当 IN 保持 TRUE 时，Q 始终为 TRUE，ET 保持为 T#0ms

## 6. TOF 功能块常见问题及解决方案

### 6.1 定时器不触发

**问题**：输入信号 IN 从 TRUE 变为 FALSE，但定时器不触发

**解决方案**：
- 检查 EN 参数是否为 TRUE
- 检查 PT 参数是否设置正确
- 检查功能块是否正确初始化
- 检查输入信号是否有下降沿（从 TRUE 变为 FALSE）

### 6.2 延时时间不准确

**问题**：实际延时时间与设定值偏差较大

**解决方案**：
- 减小 PLC 的扫描周期
- 使用更高精度的定时器功能块
- 考虑使用硬件定时器

### 6.3 定时器不复位

**问题**：输入信号 IN 变为 TRUE，但定时器不复位

**解决方案**：
- 检查 IN 参数是否确实变为 TRUE
- 检查功能块是否被其他逻辑强制保持
- 检查功能块是否正确初始化

### 6.4 输出信号异常

**问题**：输出信号 Q 的状态与预期不符

**解决方案**：
- 检查输入信号 IN 的状态变化
- 检查 PT 参数是否设置正确
- 检查功能块是否正确初始化
- 检查是否有其他逻辑影响 Q 的状态

## 7. TOF 功能块与其他定时器的比较

| 定时器类型 | 功能 | 适用场景 |
|-----------|------|----------|
| TOF | 断电延时定时器 | 延时停止、保持输出、设备冷却 |
| TON | 通电延时定时器 | 延时启动、故障检测 |
| TP | 脉冲定时器 | 生成固定宽度的脉冲 |

### 7.1 应用场景对比

- **TOF**：适用于需要在输入信号断开后保持输出一段时间的场景，如设备停机后的冷却、报警信号保持、系统断电应急处理等
- **TON**：适用于需要延时启动的场景，如电机启动前的预热、故障检测的延时确认等
- **TP**：适用于需要固定宽度脉冲的场景，如电磁阀控制、步进电机脉冲信号、报警信号等

## 8. 最佳实践

### 8.1 命名规范

- 使用有意义的变量名，如 `CoolDownTimer`、`AlarmTimer`
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

### 8.5 调试技巧

- 使用 ET 输出监控定时器的当前状态
- 在调试过程中，可临时缩短 PT 值，加快测试速度
- 使用可视化工具监控定时器的状态变化

## 9. 总结

TOF 功能块是工业自动化控制中常用的断电延时工具，通过合理使用 TOF 功能块，可以实现各种延时停止和保持输出的逻辑，如设备冷却、报警保持、应急处理等。

在使用 TOF 功能块时，应注意以下几点：

1. **正确设置参数**：根据实际需求设置合适的 PT 值和输入信号
2. **合理初始化**：在使用前正确初始化功能块
3. **注意精度**：根据应用场景选择合适的扫描周期
4. **避免冲突**：为每个定时器分配独立的变量和资源
5. **优化设计**：采用模块化设计，提高代码可维护性

通过掌握 TOF 功能块的使用方法和最佳实践，可以更高效地实现各种断电延时控制逻辑，提高控制系统的可靠性和稳定性。