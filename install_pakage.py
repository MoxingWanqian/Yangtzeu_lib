import time
import subprocess

def install_pakage(pakage):
    status, output = subprocess.getstatusoutput(f'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple {pakage}')
    if status == 0:
        print(f'Pakage of {pakage} was installed!!!')
    else:
        print('Wrong!!! ')
        print(output)

if __name__ == '__main__':
    install_pakage('requests')
    install_pakage('lxml')
    install_pakage('selenium')
    # install_pakage('pyperclip')
    print('Finish!!!')
    while True:
        time.sleep(10)