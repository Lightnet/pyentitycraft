# https://www.youtube.com/watch?v=r7Dtus7N4pI  Python Decorators in 15 Minutes

import datetime
import time

def log(func):
  def warpper(*args, **kwargs):
    with open("logs.txt","a") as f:
      f.write("Call function with " + " ".join([str(arg) for arg in args]) + " at " + str(datetime.datetime.now()) + "\n")
    val = func(*args, **kwargs)
    return val
  
  return warpper

def timer(func):
  def warpper():
    before = time.time()
    func()
    print("function took:", time.time() - before, "seconds")
  return warpper

@timer
def run():
  time.sleep(2)
#run()

@log
def run2(a,b, c=9):
  print(a+b+c)

run2(1,2,c=9)