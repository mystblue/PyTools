import os

# 実行中のカレントディレクトリをスクリプトがあるディレクトリに固定
os.chdir(os.path.dirname(os.path.abspath(__file__)))

path = os.getcwd()
print("Path = "+path)

if os.path.exists("table.txt"):
    print("table.txt は存在する")
else:
    print("table.txt は存在しない")