import time
from threading import Thread
import subprocess

COUNT = 5

def myworker():
    #print("thread start.")
    subprocess.call('php -f aws_tms_stress_test.php', shell=True)
    print("thread end.")

def main():
    print("Parent program start")
    for i in range(COUNT):
        print("thread no " + str(i + 1) + " start.")
        thread = Thread(target=myworker)
        thread.start()

if __name__ == "__main__":
    main()
