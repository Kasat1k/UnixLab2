import threading
import time
import random

class Philosopher(threading.Thread):
    def __init__(self, index, left_fork, right_fork, running):
        threading.Thread.__init__(self)
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.running = running

    def think(self):
        time.sleep(random.uniform(1, 3))
        print(f"Philosopher {self.index} is thinking.")
        
    def run(self):
        while self.running.is_set():
            self.think()
            self.dine()

    def dine(self):
        fork1, fork2 = self.left_fork, self.right_fork

        # Always try to pick the lower numbered fork first
        if self.index == 4:
            fork1, fork2 = fork2, fork1

        with fork1:
            print(f"Philosopher {self.index} picked up fork {fork1.index}.")
            with fork2:
                print(f"Philosopher {self.index} picked up fork {fork2.index}.")
                self.eat()

    def eat(self):
        print(f"Philosopher {self.index} is eating.")
        time.sleep(random.uniform(1, 3))
        print(f"Philosopher {self.index} finished eating and put down forks.")

class Fork:
    def __init__(self, index):
        self.index = index
        self.lock = threading.Lock()

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()

def main():
    num_philosophers = 5
    forks = [Fork(i) for i in range(num_philosophers)]
    running = threading.Event()
    running.set()
    philosophers = []

    for i in range(num_philosophers):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % num_philosophers]
        philosophers.append(Philosopher(i, left_fork, right_fork, running))

    for p in philosophers:
        p.start()
        
#Time of running program
    sleep_time=10
    time.sleep(sleep_time)  
    running.clear()  

    for p in philosophers:
        p.join() 

if __name__ == '__main__':
    main()
