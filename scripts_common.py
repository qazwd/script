import os
from collections import defaultdict

def first_folders_list(folder_path):
    """
    统计指定文件夹下子文件夹的数量、子文件夹名称、文件数量以及每种文件的数量。

    参数:
    folder_path (str): 要检查的文件夹的路径。

    返回:
    tuple: 包含四个元素，
           1. 子文件夹的数量；
           2. 子文件夹名称的列表；
           3. 文件夹中的文件数量；
           4. 字典，键为文件扩展名，值为该扩展名文件的数量。
    """
    # 初始化一个空列表来存储子文件夹的名称
    folder_names = []
    # 初始化文件数量
    file_count = 0
    # 初始化每种文件数量的字典
    file_type_count = defaultdict(int)
    # 检查路径是否存在
    if os.path.exists(folder_path):
        # 遍历指定路径下的所有条目
        for entry in os.listdir(folder_path):
            entry_path = os.path.join(folder_path, entry)
            # 检查条目是否为文件夹
            if os.path.isdir(entry_path):
                folder_names.append(entry)
            # 检查条目是否为文件
            elif os.path.isfile(entry_path):
                file_count += 1
                file_extension = os.path.splitext(entry)[1].lower()
                file_type_count[file_extension] += 1
    # 返回子文件夹的数量、名称列表、文件数量和每种文件的数量
    return len(folder_names), folder_names, file_count, dict(file_type_count)


import os
from collections import defaultdict

def second_folders_list(folder_path):
    """
    分析指定文件夹，返回子文件夹名称、总文件数量以及每个子文件夹的文件数量和每种文件的数量。

    参数:
    folder_path (str): 要分析的文件夹路径。

    返回:
    tuple: 包含三个元素，
           1. 子文件夹名称列表；
           2. 文件夹中的总文件数量；
           3. 字典，键为子文件夹名称，值为另一个字典，包含该子文件夹的总文件数量和每种文件的数量。
    """
    subfolder_names = []
    total_file_count = 0
    subfolder_stats = {}

    if os.path.exists(folder_path):
        # 遍历指定路径下的所有条目
        for entry in os.listdir(folder_path):
            entry_path = os.path.join(folder_path, entry)
            if os.path.isdir(entry_path):
                subfolder_names.append(entry)
                file_count = 0
                file_type_count = defaultdict(int)
                # 遍历子文件夹中的所有条目
                for root, dirs, files in os.walk(entry_path):
                    for file in files:
                        file_count += 1
                        file_extension = os.path.splitext(file)[1].lower()
                        file_type_count[file_extension] += 1
                subfolder_stats[entry] = {
                    "total_files": file_count,
                    "file_types": dict(file_type_count)
                }
                total_file_count += file_count
            elif os.path.isfile(entry_path):
                total_file_count += 1

    return subfolder_names, total_file_count, subfolder_stats

import os

def build_file_path(*path_components):
    """
    构建文件路径，支持传入多个路径组件
    
    参数:
    *path_components (str): 可变长度的路径组件参数
    
    返回:
    str: 连接后的文件路径
    """
    return os.path.join(*path_components)

from openpyxl import Workbook

def create_excel_file(file_name):
    """
    创建一个新的 Excel 文件。

    参数:
    file_name (str): 要创建的 Excel 文件的名称，需包含 .xlsx 扩展名。

    返回:
    bool: 如果文件创建成功返回 True，失败返回 False。
    """
    try:
        # 创建一个新的工作簿
        wb = Workbook()
        # 保存工作簿到指定文件
        wb.save(file_name)
        return True
    except Exception as e:
        print(f"创建 Excel 文件时出错: {e}")
        return False
    
from openpyxl import Workbook

def create_new_worksheet(workbook, sheet_name):
    """
    在指定的工作簿中创建一个新的工作表。

    参数:
    workbook (openpyxl.workbook.workbook.Workbook): 要操作的工作簿对象。
    sheet_name (str): 新工作表的名称。

    返回:
    openpyxl.worksheet.worksheet.Worksheet: 新创建的工作表对象，如果创建失败则返回 None。
    """
    try:
        # 在工作簿中创建一个新的工作表
        new_sheet = workbook.create_sheet(title=sheet_name)
        return new_sheet
    except Exception as e:
        print(f"创建工作表 {sheet_name} 时出错: {e}")
        return None
    
import os
from PIL import Image

def check_image_integrity(folder_path):
    """
    遍历指定文件夹中的所有图片，检查图片是否损坏。

    参数:
    folder_path (str): 要检查的文件夹路径。

    返回:
    tuple: 包含三个元素，
           1. 该文件夹中图片的数量；
           2. 损坏图片的数量；
           3. 损坏图片的文件路径列表。
    """
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    total_image_count = 0
    corrupted_image_count = 0
    corrupted_image_paths = []

    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(image_extensions):
                    total_image_count += 1
                    file_path = os.path.join(root, file)
                    try:
                        with Image.open(file_path) as img:
                            img.verify()
                    except Exception:
                        corrupted_image_count += 1
                        corrupted_image_paths.append(file_path)

    return total_image_count, corrupted_image_count, corrupted_image_paths


if __name__ == "__main__":
    '''
    # 指定要检查的文件夹路径
    folder_path = 'D:\\hh'

    print('-' * 50)  # 分隔线
    print(f"检查文件夹: {folder_path}")
    print('-' * 50)  # 分隔线
    folder_count, folder_names, file_count, file_type_count = first_folders_list(folder_path)
    print(f"子文件夹数量: {folder_count}")
    print(f"子文件夹名称: {folder_names}")
    print(f"文件夹中的文件数量: {file_count}")
    print("每种文件的数量:")
    for extension, count in file_type_count.items():
        print(f"  {extension}: {count}")
'''
    print("-" * 50)  # 分隔线
    '''
    folder_path = "your_folder_path"
    print("-" * 50)  # 分隔线
    print(f"检查文件夹: {folder_path}")
    subfolder_names, total_file_count, subfolder_stats = second_folders_list(folder_path)
    print(f"子文件夹名称: {subfolder_names}")
    print(f"文件夹中的总文件数量: {total_file_count}")
    print("每个子文件夹中的文件统计信息:")
    for subfolder, stats in subfolder_stats.items():
        print(f"  子文件夹: {subfolder}")
        print(f"    总文件数量: {stats['total_files']}")
        print(f"    每种文件的数量: {stats['file_types']}")
'''
    print("-" * 50)  # 分隔线
    '''
    # 构建文件路径
    file_path = build_file_path("folder", "subfolder", "file.txt")
    # 构建文件路径
    file_path = build_file_path(folder_path, 'file.txt')
    print(f"构建的文件路径: {file_path}")
    # 构建一个指向文件的路径
    config_path = build_file_path("config", "settings.ini")
    # 输出: config/settings.ini（Linux/macOS）或 config/settings.ini（Windows）
    # 构建多级目录路径
    data_path = build_file_path("home", "user", "data", "file.txt")
    # 输出: home/user/data/file.txt（Linux/macOS）或 home/user/data/file.txt（Windows）
    # 构建相对路径
    relative_path = build_file_path("..", "documents", "file.txt")
    # 输出: ..\\documents\\file.txt（Linux/macOS）或 ..\\documents\file.txt（Windows）
'''
    print("-" * 50)  # 分隔线
    '''
    # 指定要创建的 Excel 文件的名称
    file_name = "example.xlsx"
    # 创建一个新的 Excel 文件
    excel_file_name = 'example.xlsx'
    if create_excel_file(excel_file_name):
        print(f"Excel 文件 '{excel_file_name}' 创建成功。")
    else:
        print(f"Excel 文件 '{excel_file_name}' 创建失败。")
    if create_excel_file(file_name):
        print(f"{file_name} 文件创建成功。")
        wb = Workbook()
        new_sheet = create_new_worksheet(wb, "NewSheet")
        if new_sheet:
            print(f"工作表 {new_sheet.title} 创建成功。")
            wb.save(file_name)
    else:
        print(f"{file_name} 文件创建失败。")
'''
    print("-" * 50)  # 分隔线
    '''
    folder_path = "your_folder_path"
    total_images, corrupted_images, corrupted_paths = check_image_integrity(folder_path)
    print(f"该文件夹中图片的数量: {total_images}")
    print(f"损坏图片的数量: {corrupted_images}")
    print("损坏图片的文件路径:")
    for path in corrupted_paths:
        print(path)
'''
    print("-" * 50)  # 分隔线
