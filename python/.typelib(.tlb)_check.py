import comtypes.client

def view_typelib(file_path):
    """
    此函数用于查看指定路径的.typelib文件的基本信息
    :param file_path: .typelib文件的路径
    """
    try:
        # 加载Typelib文件
        typelib = comtypes.client.GetModule(file_path)

        # 打印Typelib的基本信息
        print(f"Typelib名称: {typelib.__name__}")
        print(f"Typelib版本: {typelib.__version__}")

        # 遍历Typelib中的所有类型
        for attr_name in dir(typelib):
            if not attr_name.startswith("__"):
                attr = getattr(typelib, attr_name)
                if isinstance(attr, type):
                    print(f"类型: {attr_name}")
                    # 可以进一步查看类型的属性和方法
                    for member_name in dir(attr):
                        if not member_name.startswith("__"):
                            print(f"  成员: {member_name}")
    except Exception as e:
        print(f"读取Typelib文件时出错: {e}")

# 调用函数并传入.typelib文件的路径
if __name__ == "__main__":
    typelib_file_path = "C:\\Users\\hh\\.conda\\envs\\3xpy36\\Library\\lib\\boost_chrono.lib"
    view_typelib(typelib_file_path)
