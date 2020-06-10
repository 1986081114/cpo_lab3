import unittest
from src.futures import *
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
import time



class MyTestCase(unittest.TestCase):

    def test_done (self):
        def return_future(msg):
            time.sleep(3)
            return msg

        pool = futures.ThreadPoolExecutor(max_workers=2)

        t1 = pool.submit(return_future, 'a')
        t2 = pool.submit(return_future, 'b')

        time.sleep(2)
        self.assertEqual(t1.done(), False)
        self.assertEqual(t2.done(), False)

        time.sleep(8)
        self.assertEqual(t1.done(), True)
        self.assertEqual(t2.done(), True)

    def test_process(self):
        def return_future(msg):
            time.sleep(3)
            return msg

        pool = futures.ThreadPoolExecutor(max_workers=2)

        t1 = pool.submit(return_future, 'a')
        t2 = pool.submit(return_future, 'b')
        t3 = pool.submit(return_future, 'c')
        t4 = pool.submit(return_future, 'd')
        self.assertEqual(t1.running(), True)
        self.assertEqual(t2.running(), True)
        self.assertEqual(t3.running(), False)
        self.assertEqual(t4.running(), False)


    def test_result (self):
        def return_future(msg):
            time.sleep(3)
            return msg

        pool = futures.ThreadPoolExecutor(max_workers=2)

        t1 = pool.submit(return_future, 'a')
        t2 = pool.submit(return_future, 'b')
        t1.cancel()
        self.assertEqual(t1.result(), 'a')
        self.assertEqual(t2.result(),'b')



        def task1():
            1 / 0

        def task2():
            pass

        pool = ThreadPoolExecutor(max_workers=2)
        t1 = pool.submit(task1)
        t2 = pool.submit(task2)
        try:
            t1.result()
        except Exception as e:
            print(e)  # division by zero
        self.assertEqual(t2.exception(), None)

        #  raise TimeoutError
        # t1 = pool.submit(return_future, 'a')
        # print(t1.result(timeout = 2))


    def test_cancel (self):
        def return_future(msg):
            time.sleep(3)
            return msg

        pool = futures.ThreadPoolExecutor(max_workers=2)

        t1 = pool.submit(return_future, 'a')
        t2 = pool.submit(return_future, 'b')
        t3 = pool.submit(return_future, 'c')
        t4 = pool.submit(return_future, 'd')

        self.assertEqual(t1.cancel(), False)
        self.assertEqual(t2.cancel(), False)

        self.assertEqual(t3.cancel(), True)
        self.assertEqual(t4.cancel(), True)

    def test_sequence(self):
        x = [3, 1, 2]
        y = []

        def sleeper(secs):
            time.sleep(secs)
            return secs

        # returns in the order given
        with futures.ThreadPoolExecutor(max_workers=3) as executor:
           y = list(executor.map(sleeper, x))
           self.assertEqual(y, [3,1,2])
         # [3, 1, 2]

        # returns in the order completed
        with futures.ThreadPoolExecutor(max_workers=3) as executor:
            futs = [executor.submit(sleeper, secs) for secs in x]
            y = [fut.result() for fut in futures.as_completed(futs)]
            self.assertEqual(y, [1,2,3])
        # [1, 2, 3]



if __name__ == '__main__':
    unittest.main()
