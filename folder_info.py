import os
from collections import defaultdict, deque
import math

class FolderAnalyzer:

    def __init__(self, root_dir):
        """
        初始化目录分析器
        :param root_dir: 要分析的根目录路径
        """
        self.root_dir = os.path.normpath(root_dir)
        self.total_files = 0
        self.total_file_types = defaultdict(int)  # 用于存储文件类型的数量
        self.analyzed = False                     # 用于标记是否已经分析过目录

    def analyze(self, verbose=0, max_depth=None, hidden=False):
        """
        分析目录结构
        :param verbose: 是否打印详细层级信息
        :param max_depth: 最大遍历深度（None表示无限制）
        :param hidden: 是否包含隐藏文件和文件夹
        :return: (总文件数, 文件类型统计字典)
        """
        print("\n******--------------> 文件夹统计工具 <--------------******")
        print("******----------------> 作者：qhk <----------------******")
        print("******---------------> 版本：1.0.0 <---------------******")
        print("******--------> 功能：分析文件夹结构和信息 <--------******\n")

        # 重置统计状态
        self.total_files = 0
        self.total_file_types = defaultdict(int)  # 重置文件类型统计
        self.analyzed = False                     # 标记为未分析状态
        folder = self._get_folder_name()  # 获取文件夹名称

        # 使用队列进行广度优先遍历
        queue = deque([(self.root_dir, 0)])

        if verbose == 0 or verbose == 1: 
            print(f"开始遍历文件夹: {folder}\n" + "="*50)

        while queue:                             # 当队列不为空时继续遍历
            current_dir, level = queue.popleft()  # 取出队列中的第一个元素
            # 检查是否达到最大深度
            if max_depth is not None and level > max_depth:
                continue
            try:
                items = os.listdir(current_dir)  # 获取当前目录下的所有项目
            except PermissionError:
                if verbose == 0 or verbose == 1:
                    print(f"无权限访问目录: {current_dir}")
                continue
            except FileNotFoundError:
                if verbose == 0 or verbose == 1:
                    print(f"目录不存在: {current_dir}")
                continue

            # 初始化当前层统计
            folder_names = []  # 存储文件夹名称
            file_count = 0  # 当前文件夹中的文件数量
            current_file_types = defaultdict(int)  # 当前文件夹中的文件类型统计

            # 处理当前目录下的所有项目
            for item in items:
                # 跳过隐藏文件和文件夹（如果需要）
                if not hidden and item.startswith('.'):
                    continue
                path = os.path.join(current_dir, item)  # 构建文件或文件夹的完整路径
                if os.path.isdir(path):  # 如果是文件夹
                    folder_names.append(item)  # 存储文件夹名称
                    queue.append((path, level + 1))  # 将文件夹加入队列，深度加1
                else:  # 如果是文件
                    file_count += 1  # 文件数量加1
                    # 提取文件扩展名（类型）
                    folder_name, extension = os.path.splitext(item)  # 分割文件名和扩展名
                    file_type = extension.lower() if extension else '无扩展名'  # 转换为小写，并处理无扩展名的情况
                    current_file_types[file_type] += 1  # 当前文件夹中的文件类型数量加1
                    self.total_file_types[file_type] += 1  # 总文件类型数量加1
            self.total_files += file_count  # 总文件数量加上当前文件夹中的文件数量

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

            self.analyzed = True  # 标记为已分析状态
        if verbose == 0 or verbose == 1:
            # 输出总文件数量和文件类型分布
            if verbose == 0:  # 如果verbose为1
                print('\n' + '='*50)  # 输出分隔线
            print(f' {folder}文件夹 遍历完成！')  # 输出遍历完成的提示
            print(f"|—— 总文件数量: {self.total_files}")  # 输出总文件数量
            print("└── 文件类型分布:")  # 输出文件类型分布的提示
            if self.total_files > 0:  # 如果总文件数量大于0
                for file_type, count in self.total_file_types.items():  # 遍历总文件类型和数量
                    print(f"    ├── {file_type}: {count}")  # 输出当前文件类型和数量
            else:  # 如果总文件数量为0
                print("    ├── 无文件")  # 输出无文件的提示

        print("\n******------------> 文件夹内容统计工具 <------------******\n")

        return self.total_files, dict(self.total_file_types)  # 返回总文件数量和文件类型分布
    
    def _get_folder_name(self):
        # 规范化路径（自动处理末尾分隔符和跨平台格式）
        normalized_path = os.path.normpath(self.root_dir)
        # 直接获取最后一段名称
        return os.path.basename(normalized_path)
    
    def get_folder_structure(self, max_depth=None, hidden=False):
        """
        获取目录结构信息（不打印，返回数据结构）
        :param max_depth: 最大遍历深度
        :param hidden: 是否包含隐藏文件和文件夹
        :return: 目录结构字典
        """
        structure = {}  # 初始化目录结构字典
        queue = deque([(self.root_dir, 0, structure)])  # 初始化队列，包含根目录、层级和对应的字典

        while queue:  # 当队列不为空时继续遍历
            current_dir, level, current_dict = queue.popleft()  # 取出队列中的第一个元素
            # 检查是否达到最大深度
            if max_depth is not None and level > max_depth:
                continue
            try:
                items = os.listdir(current_dir)  # 获取当前目录下的所有项目
            except (PermissionError, FileNotFoundError):
                continue  # 无权限访问目录或目录不存在，跳过

            # 初始化当前目录信息
            current_dict['path'] = current_dir  # 存储当前目录的路径
            current_dict['level'] = level  # 存储当前目录的层级
            current_dict['directories'] = []  # 存储当前目录下的文件夹名称
            current_dict['files'] = []  # 存储当前目录下的文件名称

            # 处理当前目录下的所有项目
            for item in items:
                # 跳过隐藏文件和文件夹（如果需要）
                if not hidden and item.startswith('.'):
                    continue
                path = os.path.join(current_dir, item)  # 构建文件或文件夹的完整路径
                if os.path.isdir(path):
                    dir_info = {'name': item}
                    current_dict['directories'].append(dir_info)
                    queue.append((path, level + 1, dir_info))
                else:
                    # 提取文件扩展名（类型）
                    _, ext = os.path.splitext(item)
                    file_type = ext.lower() if ext else '无扩展名'
                    current_dict['files'].append({
                        'name': item,
                        'type': file_type
                    })

        return structure  # 返回目录结构字典

    def get_total_files(self):
        """
        获取总文件数
        :return: 总文件数
        """
        if not self.analyzed:  # 如果未分析过
            self.analyze(verbose=1)  # 分析目录结构
        return self.total_files  # 返回总文件数量
    
'''
if __name__ == "__main__":
    # 示例用法：
    #folder_path = input("请输入要遍历的文件夹路径: ")
    folder_path = 'D:\\hh\\code'  # 替换为您要分析的文件夹路径

    # 创建文件夹分析器对象
    analyzer = FolderAnalyzer(folder_path)

    # 分析目录结构，verbose=0 打印详细信息，verbose=1 粗略打印信息，verbose=any 打印所有信息
    analyzer.analyze(
        verbose=0,
        max_depth=None,
        hidden=True)
    
    # 获取目录结构信息（不打印，返回数据结构）
    folder_structure = analyzer.get_folder_structure(max_depth=0, hidden=True)
    print("目录结构信息:")
    print(f"根目录: {folder_structure['path']}")  # 打印根目录路径
    print(f"层级: {folder_structure['level']}")  # 打印根目录层级
    print(f"文件夹数量: {len(folder_structure['directories'])}")  # 打印根目录下的文件夹数量
    print(f"文件数量: {len(folder_structure['files'])}")  # 打印根目录下的文件数量

    # 获取总文件数
    total_files = analyzer.get_total_files()
    print(f"总文件数: {total_files}")  # 打印总文件数
'''
