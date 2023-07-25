import os
import shutil
import subprocess
import tkinter
import tkinter.simpledialog

main = tkinter.Tk()
main.withdraw()
inputdata = tkinter.simpledialog.askstring("コメント", "コメントを入力してください", initialvalue="")
print(inputdata)

# フォルダの上書き
#shutil.copytree('src', 'dst', dirs_exist_ok=True)

os.chdir('C:\\users\\314\\Documents\\git\\PyTools')

command = 'git add .'
subprocess.call(command, shell=True)

command = 'git commit -m "' + inputdata + '"'
subprocess.call(command, shell=True)

command = 'git push origin master'
subprocess.call(command, shell=True)
