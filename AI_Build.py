import re
import sys
import os
import subprocess


def process_st_file(input_file):
    """
    处理ST文件，将 '变量名 AT %端口位置 : 变量类型;' 格式的行转换为 '变量名 : 变量类型;' 格式
    输出两个文件：
    1. generated_plc.st - 与源文件内容相同
    2. plc.st - 格式转换后的文件
    """
    # 获取源文件的绝对路径
    input_file_abs = os.path.abspath(input_file)
    # 构建输出文件路径
    directory = os.path.dirname(input_file_abs)
    original_output = os.path.join(directory, 'generated_plc.st')
    converted_output = os.path.join(directory, 'plc.st')
    
    # 定义匹配模式
    pattern = r'(\w+)\s+AT\s+%[^:]+\s*:\s*(\w+);'
    
    # 读取文件
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 1. 写入与源文件相同的文件
    with open(original_output, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    # 2. 处理并写入转换后的文件
    processed_lines = []
    for line in lines:
        # 尝试匹配模式
        match = re.match(pattern, line.strip())
        if match:
            # 提取变量名和类型
            var_name, var_type = match.groups()
            # 保持原始缩进
            indent = len(line) - len(line.lstrip())
            # 构建新行
            new_line = ' ' * indent + f'{var_name} : {var_type};' + '\n'
            processed_lines.append(new_line)
        else:
            # 非匹配行保持不变
            processed_lines.append(line)
    
    with open(converted_output, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)
    
    print(f"处理完成：")
    print(f"  与源文件相同的文件保存在: {original_output}")
    print(f"  格式转换后的文件保存在: {converted_output}")
    
    # 调用iec2c.exe处理转换后的plc.st文件
    # 计算iec2c.exe的相对路径（相对于Python脚本所在目录）
    python_dir = os.path.dirname(os.path.abspath(__file__))
    iec2c_path = os.path.join(python_dir, 'matiec', 'iec2c.exe')
    
    # 打印调试信息
    print(f"调试信息:")
    print(f"  Python脚本路径: {os.path.abspath(__file__)}")
    print(f"  Python脚本目录: {python_dir}")
    print(f"  iec2c.exe路径: {iec2c_path}")
    print(f"  iec2c.exe是否存在: {os.path.exists(iec2c_path)}")
    
    # 在调用iec2c.exe之前，检查源文件目录，如果存在plc.bin、plc文件，就删除
    print("\n检查并删除源文件目录中的plc.bin、plc文件")
    try:
        # 定义要删除的文件
        files_to_delete = ['plc.bin', 'plc']
        for file_name in files_to_delete:
            file_path = os.path.join(directory, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"  删除: {file_path}")
            else:
                print(f"  未找到: {file_path}")
    except Exception as e:
        print(f"删除文件时出错: {e}")
    
    # 检查iec2c.exe是否存在
    if os.path.exists(iec2c_path):
        # 构建命令行参数
        # 输出目录就是源文件的目录
        output_dir = directory
        lib_dir = os.path.join(os.path.dirname(iec2c_path), 'lib')
        
        # 构建完整的命令
        command = f'"{iec2c_path}" -f -l -p -I "{lib_dir}" -T "{output_dir}" "{converted_output}"'
        
        print(f"执行命令: {command}")
        
        # 执行命令
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(f"iec2c.exe执行成功！")
            print(f"输出: {result.stdout}")
            if result.stderr:
                print(f"警告: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"iec2c.exe执行失败: {e}")
            print(f"错误输出: {e.stderr}")
    else:
        print(f"警告: iec2c.exe 不存在于路径 {iec2c_path}")
        print("跳过iec2c.exe调用步骤")
    
    # 重命名符合X_CONFIG.*格式的文件为CONFIG0.*
    print("\n重命名符合X_CONFIG.*格式的文件为CONFIG0.*")
    try:
        # 遍历输出目录中的文件
        for filename in os.listdir(directory):
            # 检查文件名是否符合X_CONFIG.*格式
            if '_CONFIG.' in filename:
                # 提取文件扩展名
                ext = os.path.splitext(filename)[1]
                # 构建新文件名
                new_filename = f"CONFIG0{ext}"
                # 构建完整的文件路径
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_filename)
                # 如果目标文件已存在，先删除它
                if os.path.exists(new_path):
                    os.remove(new_path)
                    print(f"  删除已存在的文件: {new_filename}")
                # 重命名文件
                os.rename(old_path, new_path)
                print(f"  重命名: {filename} -> {new_filename}")
    except Exception as e:
        print(f"重命名文件时出错: {e}")
    
    # 修改Res0.C文件，将包含 _CONFIG.h 的行改成 #include "Config0.h"
    print("\n修改Res0.C文件中的包含语句")
    try:
        res0_path = os.path.join(directory, "Res0.c")
        if os.path.exists(res0_path):
            # 读取文件内容
            with open(res0_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # 替换包含 _CONFIG.h 的行
            modified_content = re.sub(r'#include\s*["<]([^"<]*_CONFIG\.h)[">]', '#include "Config0.h"', content)
            # 写回文件
            with open(res0_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            print(f"  成功修改: {res0_path}")
        else:
            print(f"  警告: {res0_path} 文件不存在")
    except Exception as e:
        print(f"修改Res0.C文件时出错: {e}")
    
    # 在所有生成的.h文件的第一行插入#include "beremiz.h"
    print("\n在所有.h文件的第一行插入#include \"beremiz.h\"")
    try:
        # 遍历输出目录中的文件
        for filename in os.listdir(directory):
            # 检查文件是否是.h文件
            if filename.endswith('.h'):
                # 构建完整的文件路径
                file_path = os.path.join(directory, filename)
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 在第一行插入#include "beremiz.h"
                new_content = '#include "beremiz.h"\n' + content
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  处理: {filename}")
    except Exception as e:
        print(f"处理.h文件时出错: {e}")
    
    # 复制plc_main.c和plc_debugger.c到源文件目录
    print("\n复制plc_main.c和plc_debugger.c到源文件目录")
    try:
        # 计算程序目录中的plc_main.c和plc_debugger.c路径
        python_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 检查文件是否存在
        plc_main_path = os.path.join(python_dir, "plc_main.c")
        plc_debugger_path = os.path.join(python_dir, "plc_debugger.c")
        
        if os.path.exists(plc_main_path):
            import shutil
            shutil.copy2(plc_main_path, directory)
            print(f"  复制: {plc_main_path} -> {directory}")
        else:
            print(f"  警告: {plc_main_path} 文件不存在")
        
        if os.path.exists(plc_debugger_path):
            import shutil
            shutil.copy2(plc_debugger_path, directory)
            print(f"  复制: {plc_debugger_path} -> {directory}")
        else:
            print(f"  警告: {plc_debugger_path} 文件不存在")
    except Exception as e:
        print(f"复制文件时出错: {e}")
    
    # 调用automake.bat文件，命令行参数是源文件的目录
    print("\n调用automake.bat文件")
    try:
        # 保存当前工作目录
        original_cwd = os.getcwd()
        # 设置工作目录为Python脚本所在目录（根据用户要求）
        openplc_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"切换工作目录到: {openplc_dir}")
        os.chdir(openplc_dir)
        
        # 构建命令
        # 假设automake.bat在当前目录中
        automake_bat_path = os.path.join(openplc_dir, "ESP32","automake.bat")
        command = f'"{automake_bat_path}" "{directory}"'
        print(f"执行命令: {command}")
        
        # 执行命令
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"automake.bat执行成功！")
        print(f"输出: {result.stdout}")
        if result.stderr:
            print(f"警告: {result.stderr}")
        
        # 恢复原始工作目录
        os.chdir(original_cwd)
        print(f"恢复工作目录到: {original_cwd}")
    except Exception as e:
        print(f"调用automake.bat时出错: {e}")
        # 确保恢复原始工作目录
        try:
            os.chdir(original_cwd)
        except:
            pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python AI_Build.py <input_st_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"错误: 文件 {input_file} 不存在")
        sys.exit(1)
    
    process_st_file(input_file)