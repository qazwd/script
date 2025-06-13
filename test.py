import os
from collections import defaultdict, deque
import math

def _get_folder_name(self):
        # 规范化路径（自动处理末尾分隔符和跨平台格式）
        normalized_path = os.path.normpath(folder_path)
        # 直接获取最后一段名称
        return os.path.basename(normalized_path)

def FolderAnalysis(folder_path, verbose=0, max_depth=None, hidden=False, Logo=False):
    print("\n******--------------> 文件夹分析工具 <--------------******")
    if Logo:
        print("******----------------> 作者：qhk <----------------******")
        print("******---------------> 版本：1.0.0 <---------------******")
        print("******--------> 功能：分析文件夹结构和信息 <--------******\n")

    # 初始化统计变量
    folder_path = os.path.normpath(folder_path)
    total_files = 0
    total_file_types = defaultdict(int)
    analyzed = False  # 用于标记是否已经分析过目录
    folder = _get_folder_name(folder_path)  # 获取文件夹名称

    # 使用队列进行广度优先遍历
    queue = deque([(folder_path, 0)])
    
    if verbose == 0 or verbose == 1:
        print(f"开始遍历文件夹: {folder}\n" + "="*50)

    while queue:
        current_dir, level = queue.popleft()
        # 检查是否达到最大深度
        if max_depth is not None and level > max_depth:
            continue
        try:
            items = os.listdir(current_dir)  # 获取当前目录下的所有项目
        except (PermissionError):
            if verbose == 0 or verbose == 1:
                print(f"无权限访问目录: {current_dir}")
            continue
        except FileNotFoundError:
            if verbose == 0 or verbose == 1:
                print(f"目录不存在: {current_dir}")
            continue
        except OSError as e:
            if verbose == 0 or verbose == 1:
                print(f"访问目录时发生错误: {e}")
            continue
        except Exception as e:
            if verbose == 0 or verbose == 1:
                print(f"发生未知错误: {e}")
            continue

        # 初始化当前层统计
        folder_names = []
        file_count = 0
        current_file_types = defaultdict(int)

        # 遍历当前层项目
        for item in items:
            # 跳过隐藏文件和文件夹（如果需要）
            if not hidden and item.startswith('.'):
                continue
            path = os.path.join(current_dir, item)
            if os.path.isdir(path):
                folder_names.append(item)  # 存储文件夹名称
                queue.append((path, level + 1))
            else:
                file_count += 1
                _folder_name, extension = os.path.splitext(item)
                file_type = extension.lower() if extension else '无扩展名'
                current_file_types[file_type] += 1
                total_file_types[file_type] += 1
        total_files += file_count

        # 如果verbose为0，打印当前层信息
        if verbose == 0:
            # 输出当前层信息
            indent = "│   " * level  # 根据层级生成缩进
            print(f"{indent}├── [层级 {level}] {current_dir}")  # 输出当前文件夹的路径和层级
            print(f"{indent}│   ├── 文件夹数量: {len(folder_names)}")  # 输出当前文件夹中的文件夹数量
            print(f"{indent}│   ├── 文件数量: {file_count}")  # 输出当前文件夹中的文件数量
            # 输出文件夹名称（每行最多显示10个）
            if folder_names:  # 如果有文件夹
                print(f"{indent}│   ├── 文件夹名称:")  # 输出文件夹名称的提示
                per_line = 10  # 每行显示的文件夹数量
                lines = math.ceil(len(folder_names) / per_line)  # 计算需要的行数
                for i in range(lines):  # 遍历每一行
                    start = i * per_line  # 计算当前行的起始索引
                    end = start + per_line  # 计算当前行的结束索引
                    folders_line = ', '.join(folder_names[start:end])  # 拼接当前行的文件夹名称
                    print(f"{indent}│   │   ├── {folders_line}")  # 输出当前行的文件夹名称
            else:  # 如果没有文件夹
                print(f"{indent}│   ├── 文件夹名称: 无")  # 输出无文件夹的提示
            if file_count > 0:  # 如果当前文件夹中有文件
                print(f"{indent}|   |—— 文件类型分布:")  # 输出文件类型分布的提示
                for file_type, count in current_file_types.items():  # 遍历当前文件夹中的文件类型和数量
                    print(f"{indent}│   │   ├── {file_type}: {count}")  # 输出当前文件类型和数量
            else:  # 如果当前文件夹中没有文件
                print(f"{indent}│   │   ├── 无文件")  # 输出无文件的提示
            if folder_names:
                print(f"{indent}\n{indent}▼")  # 输出文件夹展开的提示
            else:
                print(f"{indent}|")  # 输出文件夹结束的提示

        analyzed = True  # 标记已分析过目录
        
    # 输出总统计信息
    if verbose == 0 or verbose == 1:
        if verbose == 0:
            print("\n" + "="*50)
        print(f"文件夹: {folder} 分析完成!")
        print(f"|——总文件数量: {total_files}")
        print("└──文件类型分布:")
        if total_files > 0:
            for file_type, count in total_file_types.items():
                print(f"    ├── {file_type}: {count}")
        else:
            print("    ├── 无文件")
        
    print("\n******------------> 文件夹内容统计工具 <------------******\n")

    return total_files, dict(total_file_types)


# 调用示例
if __name__ == "__main__":
    
    #folder_path = input("请输入要遍历的文件夹路径: ")
    folder_path = 'D:\\hh\\code'  # 替换为您要分析的文件夹路径
    
    # 分析目录结构，verbose=0 打印详细信息，verbose=1 粗略打印信息
    FolderAnalysis(
        folder_path,
        verbose=0,
        max_depth=None,
        hidden=True,
        Logo=True
    )
'''
    # 获取该路径下总文件数和文件类型分布
    total_files = FolderAnalysis(folder_path)
    print(f"总文件数: {total_files}")
'''
