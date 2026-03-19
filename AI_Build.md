# AI_Build.py 说明文档

## 项目概述

AI_Build.py 是一个用于处理 ST (Structured Text) 文件并构建 PLC 项目的自动化脚本。它主要用于将 ST 文件中的变量声明格式转换为标准格式，并执行一系列构建步骤，最终生成可用于 ESP32 平台的 PLC 可执行文件。

## 功能说明

AI_Build.py 执行以下功能：

1. **ST 文件处理**：将 ST 文件中 `变量名 AT %端口位置 : 变量类型;` 格式的行转换为 `变量名 : 变量类型;` 格式
2. **文件生成**：
   - 生成 `generated_plc.st` - 与源文件内容相同
   - 生成 `plc.st` - 格式转换后的文件
3. **清理旧文件**：在调用 iec2c.exe 之前，删除源文件目录中的 `plc.bin` 和 `plc` 文件
4. **代码生成**：调用 iec2c.exe 将 plc.st 转换为 C 代码
5. **文件重命名**：将符合 `X_CONFIG.*` 格式的文件重命名为 `CONFIG0.*`
6. **文件修改**：
   - 修改 `Res0.c` 文件中的包含语句，将 `_CONFIG.h` 改为 `Config0.h`
   - 在所有 `.h` 文件的第一行插入 `#include "beremiz.h"`
7. **文件复制**：将 `plc_main.c` 和 `plc_debugger.c` 复制到源文件目录
8. **构建项目**：调用 `automake.bat` 构建项目，生成最终的可执行文件

## 安装要求

1. **Python 3.x**：确保系统已安装 Python 3.x 版本
2. **matiec 编译器**：脚本需要使用 matiec 目录下的 iec2c.exe 编译器
3. **ESP32 构建环境**：需要 ESP32 目录下的 automake.bat 构建脚本
4. **依赖文件**：
   - `plc_main.c`：主程序文件
   - `plc_debugger.c`：调试器文件

## 使用方法

### 基本用法

```bash
python AI_Build.py <input_st_file>
```

### 示例

```bash
# 处理 test 目录中的 AI_PDM.st 文件
python AI_Build.py test\AI_PDM.st
```

## 工作流程

1. **输入处理**：接收用户提供的 ST 文件路径
2. **文件转换**：处理 ST 文件，生成 `generated_plc.st` 和 `plc.st`
3. **清理旧文件**：删除源文件目录中的 `plc.bin` 和 `plc` 文件
4. **代码生成**：调用 iec2c.exe 将 plc.st 转换为 C 代码
5. **文件处理**：
   - 重命名 `X_CONFIG.*` 文件为 `CONFIG0.*`
   - 修改 `Res0.c` 中的包含语句
   - 在 `.h` 文件中插入 `#include "beremiz.h"`
6. **文件复制**：复制 `plc_main.c` 和 `plc_debugger.c` 到源文件目录
7. **项目构建**：调用 `automake.bat` 构建项目

## 输出文件

执行脚本后，源文件目录中会生成以下文件：

- `generated_plc.st`：与源文件内容相同的文件
- `plc.st`：格式转换后的文件
- `POUS.c`、`POUS.h`：生成的 C 代码文件
- `LOCATED_VARIABLES.h`：变量定位文件
- `VARIABLES.csv`：变量 CSV 文件
- `CONFIG0.c`、`CONFIG0.h`：重命名后的配置文件
- `Res0.c`：修改后的资源文件
- `plc_main.c`、`plc_debugger.c`：复制的主程序和调试器文件
- `plc.bin`、`plc`：最终生成的可执行文件

## 注意事项

1. **路径要求**：
   - `iec2c.exe` 必须位于 `matiec` 目录中
   - `automake.bat` 必须位于 `ESP32` 目录中
   - `plc_main.c` 和 `plc_debugger.c` 必须与脚本在同一目录

2. **权限要求**：脚本需要对源文件目录有读写权限

3. **错误处理**：脚本包含基本的错误处理，如文件不存在时的警告

## 故障排除

1. **iec2c.exe 执行失败**：
   - 检查 `matiec` 目录是否存在
   - 检查 `iec2c.exe` 是否存在且可执行

2. **automake.bat 执行失败**：
   - 检查 `ESP32` 目录是否存在
   - 检查 `automake.bat` 是否存在且可执行

3. **文件复制失败**：
   - 检查 `plc_main.c` 和 `plc_debugger.c` 是否存在
   - 检查源文件目录是否有写权限

4. **文件不存在警告**：
   - 脚本会在文件不存在时显示警告，但会继续执行其他步骤

## 示例输出

```
处理完成：
  与源文件相同的文件保存在: C:\Users\zhouweixian\Documents\trae_projects\autobuild\test\generated_plc.st
  格式转换后的文件保存在: C:\Users\zhouweixian\Documents\trae_projects\autobuild\test\plc.st
调试信息:
  Python脚本路径: C:\Users\zhouweixian\Documents\trae_projects\autobuild\AI_Build.py
  Python脚本目录: C:\Users\zhouweixian\Documents\trae_projects\autobuild
  iec2c.exe路径: C:\Users\zhouweixian\Documents\trae_projects\autobuild\matiec\iec2c.exe
  iec2c.exe是否存在: True

检查并删除源文件目录中的plc.bin、plc文件
  删除: C:\Users\zhouweixian\Documents\trae_projects\autobuild\test\plc
  未找到: C:\Users\zhouweixian\Documents\trae_projects\autobuild\test\plc.bin
执行命令: "C:\Users\zhouweixian\Documents\trae_projects\autobuild\matiec\iec2c.exe" -f -l -p -I "C:\Users\zhouweixian\Documents\trae_projects\autobuild\matiec\lib" -T "C:\Users\zhouweixian\Documents\trae_projects\autobuild\test" "C:\Users\zhouweixian\Documents\trae_projects\autobuild\test\plc.st"
iec2c.exe执行成功！
输出: POUS.c
POUS.h
LOCATED_VARIABLES.h
VARIABLES.csv
AI_PDM_CONFIG.c
AI_PDM_CONFIG.h
Res0.c


重命名符合X_CONFIG.*格式的文件为CONFIG0.*
  删除已存在的文件: CONFIG0.c
  重命名: AI_PDM_CONFIG.c -> CONFIG0.c
  删除已存在的文件: CONFIG0.h
  重命名: AI_PDM_CONFIG.h -> CONFIG0.h

修改Res0.C文件中的包含语句
  成功修改: C:\Users\zhouweixian\Documents\trae_projects\autobuild\test\Res0.c

在所有.h文件的第一行插入#include "beremiz.h"
  处理: CONFIG0.h
  处理: LOCATED_VARIABLES.h
  处理: POUS.h

复制plc_main.c和plc_debugger.c到源文件目录
  复制: C:\Users\zhouweixian\Documents\trae_projects\autobuild\plc_main.c -> C:\Users\zhouweixian\Documents\trae_projects\autobuild\test
  复制: C:\Users\zhouweixian\Documents\trae_projects\autobuild\plc_debugger.c -> C:\Users\zhouweixian\Documents\trae_projects\autobuild\test

调用automake.bat文件
切换工作目录到: C:\Users\zhouweixian\Documents\trae_projects\autobuild
执行命令: "C:\Users\zhouweixian\Documents\trae_projects\autobuild\ESP32\automake.bat" "C:\Users\zhouweixian\Documents\trae_projects\autobuild\test"
automake.bat执行成功！
输出: ...
```

## 版本历史

- **v1.0**：初始版本，实现基本的 ST 文件处理和构建功能
- **v1.1**：添加了在调用 iec2c.exe 之前删除旧文件的功能
- **v1.2**：改进了错误处理和日志输出

## 联系方式

如有任何问题或建议，请联系项目维护者。