# -*- coding: utf-8 -*-
import time
from threading import Thread
import subprocess

COUNT = 30

def myworker():
    #print("thread start.")
    subprocess.call('vendor/bin/phpunit --filter "test_sbps" tests/Feature/gwUnitTests.php', shell=True)
    print("thread end.")

def main():
    t1 = time.time() 

    th_list = []

    print("Parent program start")
    for i in range(COUNT):
        print("thread no " + str(i + 1) + " start.")
        thread = Thread(target=myworker)
        thread.start()
        th_list.append(thread)

    for thread in th_list:
        thread.join()

    t2 = time.time()
    elapsed_time = t2-t1
    print("process time = {0}".format(elapsed_time))

if __name__ == "__main__":
    main()
