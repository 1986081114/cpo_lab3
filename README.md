#                             cpo_lab3



Computational Process Organization lab3

## title: Futures with worker pool

## list of group members

- Zhao Ji
  - ID: 192050213
  - Email :1986081114@qq.com
- Duan Shoujian
  - ID: 192050215

## laboratory work number: 4

## variant description

In this variant, we implement a futures library . For that, we use done , cancel,  result, submit, map methods to run.

## synopsis

work of Zhao Ji &Duan Shoujian :

1. implement the following API:
   - IsDone() – return True if future evaluation is complete;
   - InProgress() – return True if future evaluated right now;
   - Result(timeout=None)
        return the future execution result (if the future is done);
        raise the exception (if the future is done and raise an exception);
        block until future is done (if the timeout is None and future is not done);
       raise TimeoutError after timeout (if the timeout is not None and the future is not    done).
   - map(List, Function) and reduce(List, Function, Initial State).
   - Cancel() – cancel a future (if the future not executed).
2. To proof correctness, we write unit tests, properties-based tests.

## descriptions of modules

in the module of futures: 

-    def cancel(self):
-    def result(self, timeout=None):
-    def running(self):
-    def exception(self, timeout=None):
-  def submit(self, fn, *args, **kwargs):
-  def shutdown(self, wait=True):



## conclusion

The Python Futures module, located in concurrent.futures and asyncio, both represent operations with delays. Futures will wrap the operations in the waiting state and put them in the queue. The status of these operations can be queried at any time. Of course, their results (or exceptions) can also be obtained after the operation is completed. Using futures in some ways can greatly reduce time

