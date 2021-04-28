from threading import Condition


class Semaphore:
    _counter: int
    _capacity: int
    _condition: Condition

    def __init__(self, capacity: int = 1) -> None:
        if capacity < 0:
            raise ValueError("The capacity must be non-negative.")

        self._counter = capacity
        self._capacity = capacity
        self._condition = Condition()

    def acquire(self) -> None:
        with self._condition:
            while self._counter == 0:
                self._condition.wait()
            self._counter -= 1

    def release(self) -> None:
        with self._condition:
            if self._counter < self._capacity:
                self._counter += 1
                self._condition.notify()
            else:
                raise ValueError("The number of threads that the semaphore can release has been exceeded.")

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
