import os
from collections import defaultdict, deque

class DirectoryAnalyzer:
    def __init__(self, root_dir):
        """
        初始化目录分析器
        :param root_dir: 要分析的根目录路径
        """
        self.root_dir = os.path.abspath(os.path.normpath(root_dir))
        self.total_files = 0
        self.total_file_types = defaultdict(int)
        self.analyzed = False
        self.layer_stats = []
    
    def analyze(self, verbose=True, max_depth=None, include_hidden=False, show_folders=True):
        """
        分析目录结构
        :param verbose: 是否打印详细层级信息
        :param max_depth: 最大遍历深度（None表示无限制）
        :param include_hidden: 是否包含隐藏文件和文件夹
        :param show_folders: 是否显示文件夹名称
        :return: (总文件数, 文件类型统计字典)
        """
        # 重置统计状态
        self._reset_stats()
        
        # 使用队列进行广度优先遍历
        queue = deque([(self.root_dir, 0)])
        
        if verbose:
            print(f"📁 开始遍历目录: {self.root_dir}")
            print("=" * 60)
        
        while queue:
            current_dir, level = queue.popleft()
            
            # 检查是否达到最大深度
            if max_depth is not None and level > max_depth:
                continue
            
            # 获取当前目录内容
            dirs, files, file_types = self._scan_directory(current_dir, include_hidden)
            
            # 更新统计信息
            self._update_stats(len(files), file_types)
            
            # 存储层级统计信息
            self.layer_stats.append({
                'path': current_dir,
                'level': level,
                'dir_count': len(dirs),
                'dir_names': dirs,
                'file_count': len(files),
                'file_types': dict(file_types)
            })
            
            # 添加子目录到队列
            for d in dirs:
                queue.append((os.path.join(current_dir, d), level + 1))
            
            # 打印当前层信息
            if verbose:
                self._print_layer_info(level, current_dir, dirs, files, file_types, show_folders)
        
        # 标记为已分析
        self.analyzed = True
        
        # 打印最终统计
        if verbose:
            self._print_final_stats()
        
        return self.total_files, dict(self.total_file_types)
    
    def get_summary(self):
        """
        获取分析摘要
        :return: (总文件数, 文件类型统计字典)
        """
        if not self.analyzed:
            self.analyze(verbose=False)
        return self.total_files, dict(self.total_file_types)
    
    def get_layer_stats(self, level=None):
        """
        获取层级统计信息
        :param level: 指定层级（None表示所有层级）
        :return: 层级统计信息列表
        """
        if not self.analyzed:
            self.analyze(verbose=False)
        
        if level is None:
            return self.layer_stats
        
        return [stat for stat in self.layer_stats if stat['level'] == level]
    
    def get_top_file_types(self, n=5):
        """
        获取前n个最常见的文件类型
        :param n: 返回的类型数量
        :return: 排序后的文件类型列表 [(类型, 数量), ...]
        """
        if not self.analyzed:
            self.analyze(verbose=False)
        
        sorted_types = sorted(self.total_file_types.items(), 
                             key=lambda x: x[1], reverse=True)
        return sorted_types[:n]
    
    def quick_scan(self):
        """
        快速扫描根目录（不递归子目录）
        :return: (文件夹数, 文件数, 文件类型统计)
        """
        _, dirs, files = self._scan_directory(self.root_dir, include_hidden=False)
        file_types = defaultdict(int)
        
        for file in files:
            _, ext = os.path.splitext(file)
            file_type = ext.lower() if ext else '无扩展名'
            file_types[file_type] += 1
        
        return len(dirs), len(files), dict(file_types)
    
    def _reset_stats(self):
        """重置统计信息"""
        self.total_files = 0
        self.total_file_types.clear()
        self.layer_stats = []
        self.analyzed = False
    
    def _scan_directory(self, path, include_hidden):
        """扫描目录内容"""
        try:
            items = os.listdir(path)
        except Exception as e:
            if isinstance(e, (PermissionError, FileNotFoundError)):
                return [], [], defaultdict(int)
            raise
        
        dirs = []
        files = []
        
        for item in items:
            if not include_hidden and item.startswith('.'):
                continue
            
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                dirs.append(item)
            else:
                files.append(item)
        
        # 统计文件类型
        file_types = defaultdict(int)
        for file in files:
            _, ext = os.path.splitext(file)
            file_type = ext.lower() if ext else '无扩展名'
            file_types[file_type] += 1
        
        return dirs, files, file_types
    
    def _update_stats(self, file_count, file_types):
        """更新全局统计信息"""
        self.total_files += file_count
        for ftype, count in file_types.items():
            self.total_file_types[ftype] += count
    
    def _print_layer_info(self, level, path, dirs, files, file_types, show_folders):
        """打印当前层级信息"""
        indent = "│   " * level
        print(f"{indent}├── [层级 {level}] {path}")
        print(f"{indent}│   ├── 文件夹: {len(dirs)}个")
        
        # 显示文件夹名称（如果启用）
        if show_folders and dirs:
            # 最多显示5个文件夹名称
            display_dirs = dirs[:5]
            dirs_str = ", ".join(display_dirs)
            if len(dirs) > 5:
                dirs_str += f", ...等{len(dirs)}个文件夹"
            print(f"{indent}│   │   ├── {dirs_str}")
        
        print(f"{indent}│   ├── 文件: {len(files)}个")
        
        if files:
            # 最多显示3个文件类型
            print(f"{indent}│   ├── 文件类型:")
            sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)
            for ftype, count in sorted_types[:3]:
                print(f"{indent}│   │   ├── {ftype}: {count}个")
            if len(file_types) > 3:
                print(f"{indent}│   │   ├── ...等{len(file_types)}种类型")
        else:
            print(f"{indent}│   ├── 文件类型: 无文件")
        
        # 显示下一层指示器
        if dirs:
            print(f"{indent}│\n{indent}▼")
        else:
            print(f"{indent}│")
    
    def _print_final_stats(self):
        """打印最终统计结果"""
        print("\n" + "=" * 60)
        print(f"✅ 遍历完成! 共扫描 {len(self.layer_stats)} 个目录")
        print(f"📊 总计统计:")
        print(f"├── 总文件数: {self.total_files}")
        
        if self.total_files > 0:
            print(f"└── 文件类型分布:")
            # 显示前5种文件类型
            top_types = self.get_top_file_types(5)
            for i, (ftype, count) in enumerate(top_types):
                prefix = "├──" if i < len(top_types) - 1 else "└──"
                percent = count / self.total_files * 100
                print(f"    {prefix} {ftype}: {count}个 ({percent:.1f}%)")
            
            # 显示其他类型
            other_count = self.total_files - sum(count for _, count in top_types)
            if other_count > 0:
                percent = other_count / self.total_files * 100
                print(f"    └── 其他: {other_count}个 ({percent:.1f}%)")
        else:
            print(f"└── 文件类型: 无文件")
        
        print("=" * 60)


# 使用示例
if __name__ == "__main__":
    path = 'D:\\hh\\code'

    # 创建分析器实例
    analyzer = DirectoryAnalyzer(path)
    
    # 示例1: 完整分析并打印结果
    print("完整分析:")
    analyzer.analyze()
    
    # 示例2: 快速扫描根目录
    print("\n快速扫描:")
    dir_count, file_count, file_types = analyzer.quick_scan()
    print(f"根目录: {analyzer.root_dir}")
    print(f"文件夹: {dir_count}个, 文件: {file_count}个")
    if file_types:
        print("文件类型:")
        for ftype, count in file_types.items():
            print(f"  {ftype}: {count}个")
    
    # 示例3: 获取摘要信息
    print("\n摘要统计:")
    total_files, file_types = analyzer.get_summary()
    print(f"总文件数: {total_files}")
    top_types = analyzer.get_top_file_types(3)
    print("最常见文件类型:")
    for ftype, count in top_types:
        print(f"  {ftype}: {count}个")
    
    # 示例4: 获取特定层级统计
    print("\n层级统计 (level=1):")
    layer_stats = analyzer.get_layer_stats(level=1)
    for stat in layer_stats:
        print(f"[层级 {stat['level']}] {stat['path']}")
        print(f"  文件夹: {stat['dir_count']}个, 文件: {stat['file_count']}个")
