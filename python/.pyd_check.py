import pefile

# 替换为你的 .pyd 文件路径
pyd_file = 'C:\\Users\\hh\\.conda\\envs\\3xpy36\\DLLs\\_asyncio.pyd'

try:
    pe = pefile.PE(pyd_file)
    print("Sections:")
    for section in pe.sections:
        # 提前处理去除空字符
        section_name = section.Name.decode().rstrip('\x00')
        print(f"  Name: {section_name}, Size: {section.SizeOfRawData}")
    
    print("\nImports:")
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            print(f"  DLL: {entry.dll.decode()}")
            for imp in entry.imports:
                print(f"    Function: {imp.name.decode() if imp.name else imp.ordinal}")
except Exception as e:
    print(f"Error: {e}")
