import os
from collections import defaultdict, deque
import math

class DirectoryAnalyzer:
    def __init__(self, root_dir):
        """
        初始化目录分析器
        :param root_dir: 要分析的根目录路径
        """
        self.root_dir = os.path.normpath(root_dir)
        self.total_files = 0
        self.total_file_types = defaultdict(int)
        self.analyzed = False
    
    def analyze(self, verbose=True, max_depth=None, include_hidden=False):
        """
        分析目录结构
        :param verbose: 是否打印详细层级信息
        :param max_depth: 最大遍历深度（None表示无限制）
        :param include_hidden: 是否包含隐藏文件和文件夹
        :return: (总文件数, 文件类型统计字典)
        """
        # 重置统计状态
        self.total_files = 0
        self.total_file_types = defaultdict(int)
        self.analyzed = False
        
        # 使用队列进行广度优先遍历
        queue = deque([(self.root_dir, 0)])
        
        if verbose:
            print(f"开始遍历目录: {self.root_dir}\n" + "="*50)
        
        while queue:
            current_dir, level = queue.popleft()
            
            # 检查是否达到最大深度
            if max_depth is not None and level > max_depth:
                continue
            
            try:
                items = os.listdir(current_dir)
            except PermissionError:
                if verbose:
                    print(f"无权限访问目录: {current_dir}")
                continue
            except FileNotFoundError:
                if verbose:
                    print(f"目录不存在: {current_dir}")
                continue
            
            # 初始化当前层统计
            dir_names = []  # 存储文件夹名称
            file_count = 0
            current_file_types = defaultdict(int)
            
            # 处理当前目录下的所有项目
            for item in items:
                # 跳过隐藏文件和文件夹（如果需要）
                if not include_hidden and item.startswith('.'):
                    continue
                
                path = os.path.join(current_dir, item)
                
                if os.path.isdir(path):
                    dir_names.append(item)
                    queue.append((path, level + 1))
                else:
                    file_count += 1
                    # 提取文件扩展名（类型）
                    _, ext = os.path.splitext(item)
                    file_type = ext.lower() if ext else '无扩展名'
                    current_file_types[file_type] += 1
                    self.total_file_types[file_type] += 1
            
            self.total_files += file_count
            
            # 如果verbose为True，打印当前层信息
            if verbose:
                indent = "│   " * level
                print(f"{indent}├── [层级 {level}] {current_dir}")
                print(f"{indent}│   ├── 文件夹数量: {len(dir_names)}")
                
                # 输出文件夹名称（每行最多显示5个）
                if dir_names:
                    print(f"{indent}│   ├── 文件夹列表:")
                    per_line = 5
                    lines = math.ceil(len(dir_names) / per_line)
                    
                    for i in range(lines):
                        start = i * per_line
                        end = start + per_line
                        dirs_line = ", ".join(dir_names[start:end])
                        print(f"{indent}│   │   ├── {dirs_line}")
                else:
                    print(f"{indent}│   ├── 文件夹列表: 无")
                
                print(f"{indent}│   ├── 文件数量: {file_count}")
                
                if file_count > 0:
                    print(f"{indent}│   ├── 文件类型统计:")
                    for ftype, count in current_file_types.items():
                        print(f"{indent}│   │   ├── {ftype}: {count}个")
                else:
                    print(f"{indent}│   ├── 文件类型统计: 无文件")
                
                # 显示下一层指示器
                if dir_names:
                    print(f"{indent}│\n{indent}▼")
                else:
                    print(f"{indent}│")
        
        # 标记为已分析
        self.analyzed = True
        
        if verbose:
            # 输出最终统计结果
            print("\n" + "="*50)
            print(f"遍历完成！总计统计:")
            print(f"├── 总文件数量: {self.total_files}")
            print(f"└── 文件类型分布:")
            
            if self.total_files > 0:
                for ftype, count in sorted(self.total_file_types.items(), key=lambda x: x[1], reverse=True):
                    print(f"    ├── {ftype}: {count}个")
            else:
                print("    无任何文件")
        
        return self.total_files, dict(self.total_file_types)
    
    def get_summary(self):
        """
        获取分析摘要
        :return: (总文件数, 文件类型统计字典)
        """
        if not self.analyzed:
            self.analyze(verbose=False)
        return self.total_files, dict(self.total_file_types)
    
    def get_file_type_distribution(self):
        """
        获取文件类型分布
        :return: 文件类型统计字典
        """
        if not self.analyzed:
            self.analyze(verbose=False)
        return dict(self.total_file_types)
    
    def get_total_files(self):
        """
        获取总文件数
        :return: 总文件数
        """
        if not self.analyzed:
            self.analyze(verbose=False)
        return self.total_files
    
    def get_directory_structure(self, max_depth=None, include_hidden=False):
        """
        获取目录结构信息（不打印，返回数据结构）
        :param max_depth: 最大遍历深度
        :param include_hidden: 是否包含隐藏文件
        :return: 目录结构字典
        """
        structure = {}
        queue = deque([(self.root_dir, 0, structure)])
        
        while queue:
            current_dir, level, current_dict = queue.popleft()
            
            # 检查是否达到最大深度
            if max_depth is not None and level > max_depth:
                continue
            
            try:
                items = os.listdir(current_dir)
            except (PermissionError, FileNotFoundError):
                continue
            
            # 初始化当前目录信息
            current_dict['path'] = current_dir
            current_dict['level'] = level
            current_dict['directories'] = []
            current_dict['files'] = []
            
            # 处理当前目录下的所有项目
            for item in items:
                # 跳过隐藏文件和文件夹（如果需要）
                if not include_hidden and item.startswith('.'):
                    continue
                
                path = os.path.join(current_dir, item)
                
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
        
        return structure


# 使用示例
if __name__ == "__main__":
    path = 'D:\\hh\\code'

    # 创建分析器实例
    analyzer = DirectoryAnalyzer(path)
    
    # 方式1: 完整分析并打印详细结果
    total_files, file_types = analyzer.analyze(
        verbose=True, 
        max_depth=3, 
        include_hidden=False
    )
    print("--------------")

    # 方式2: 只获取摘要信息（不打印）
    total_files = analyzer.get_total_files()
    file_types = analyzer.get_file_type_distribution()
    
    print(f"\n总文件数: {total_files}")
    print("文件类型分布:")
    for ftype, count in file_types.items():
        print(f"  {ftype}: {count}")
    print("--------------")
    
    # 方式3: 获取目录结构数据
    structure = analyzer.get_directory_structure(max_depth=2, include_hidden=True)
    print("\n目录结构摘要:")
    print(f"根目录: {structure['path']}")
    print(f"一级子目录数: {len(structure['directories'])}")
    print(f"根目录下文件数: {len(structure['files'])}")
    print("--------------")
    
    # 方式4: 仅统计根目录
    root_stats = DirectoryAnalyzer(path)
    root_stats.analyze(max_depth=0, verbose=True)
