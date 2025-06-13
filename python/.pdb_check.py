import pdbparse

def view_pdb(file_path):
    try:
        # 打开 PDB 文件
        with pdbparse.parse(file_path) as pdb:
            # 打印基本信息
            print(f"PDB 文件签名: {pdb.Signature}")
            print(f"PDB 文件版本: {pdb.DBI.Version}")

            # 遍历全局符号
            if hasattr(pdb.DBI, 'GlobalSymbols'):
                for symbol in pdb.DBI.GlobalSymbols:
                    print(f"全局符号: {symbol.name}")

            # 遍历公共符号
            if hasattr(pdb.DBI, 'PublicSymbols'):
                for symbol in pdb.DBI.PublicSymbols:
                    print(f"公共符号: {symbol.name}")

    except Exception as e:
        print(f"读取 PDB 文件时出错: {e}")

if __name__ == "__main__":
    pdb_file_path = "C:/Users/hh/.conda/envs/3xpy36/Library/lib/engines-1_1/padlock.pdb"
    view_pdb(pdb_file_path)
