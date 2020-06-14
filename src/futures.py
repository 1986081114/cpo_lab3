import queue
import threading



class TimeoutError(Exception):
    def __init__(self):
        self.msg = 'error: TimeoutError'
        print(self.msg)


class CancelledError(Exception):
    def __init__(self):
        self.msg = 'error:Future has been cancelled.'
        print(self.msg)


class Future(object):
    def __init__(self):
        self._result = None
        self._condition = threading.Condition()
        self._state = 'PENDING'

    def done(self):
        with self._condition:
            return self._state == 'FINISHED'

    def running(self):
        with self._condition:
            return self._state == 'RUNNING'

    def cancelled(self):
        with self._condition:
            return self._state == 'CANCELLED'

    def result(self, timeout=None):
        with self._condition:
            if self._state == 'CANCELLED':
                raise CancelledError()
            elif self._state == 'FINISHED':
                return self._result
            self._condition.wait(timeout)  # Block until future is done.
            if self._state == 'CANCELLED':
                raise CancelledError()
            elif self._state == 'FINISHED':
                return self._result
            else:
                raise TimeoutError()  # Timeout.

    def cancel(self):
        if self._state in ['RUNNING', 'FINISHED']:
            return False
        else:
            self.set_cancelled()

    def set_result(self, result):
        with self._condition:
            self._result = result
            self._state = 'FINISHED'
            self._condition.notify_all()

    def set_running(self):
        self._state = 'RUNNING'

    def set_cancelled(self):
        self._state = 'CANCELLED'


class ThreadPoolExecutor(object):

    def __init__(self, max_workers=None, priority=False):
        if max_workers is None:
            max_workers = 4
        elif max_workers <= 0:
            raise ValueError('max_workers must be greater than 0')

        self._max_workers = max_workers
        self._work_queue = queue.Queue()
        self._threads = set()

    def submit(self, fn, *args, **kwargs):
        f = Future()
        w = _WorkItem(None, f, fn, args, kwargs)
        self._work_queue.put(w)
        if len(self._threads) < self._max_workers:
            t = threading.Thread(target=_worker, args=(self._work_queue,))
            t.daemon = True
            t.start()
            self._threads.add(t)

        return f

    def submit_with_priority(self, fn_dict):
        fs = []
        for fn in fn_dict.keys():
            f = Future()
            fs.append(f)
            w = _WorkItem(fn_dict[fn]['priority'], f, fn, fn_dict[fn]['args'])
            self._work_queue.put(w)
        for thread_num in range(self._max_workers):
            self._start_working()
        return fs

    def shutdown(self):
        self._work_queue.join()

    def map(self, fn, *iterables, timeout=None, chunksize=1):
        pass

    def _start_working(self):
        """
        Wake worker thread.
        """
        if len(self._threads) < self._max_workers:  # Running threads must smaller than maximum.
            t = threading.Thread(target=_worker, args=(self._work_queue,))
            t.daemon = True  # When main thread quits, children threads quit as well.
            t.start()
            self._threads.add(t)


def _worker(work_queue, priority=False):
    while True:
        work_item = work_queue.get(block=True)
        if work_item is not None:
            work_item.run()
            del work_item
            work_queue.task_done()
            continue


class _WorkItem(object):
    def __init__(self, priority, future, fn, args, kwargs=None):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.priority = priority

    def run(self):
        self.future.set_running()
        if self.kwargs is None:
            result = self.fn(*self.args)
        else:
            result = self.fn(*self.args, *self.kwargs)
        self.future.set_result(result)

    def __lt__(self, other):
        return self.priority <= other.priority
