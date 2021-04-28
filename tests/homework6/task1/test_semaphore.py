import time
import unittest
from threading import Thread, Lock

from homeworks.homework6.task1.semaphore import Semaphore
from tests.test_utils import check_error_message

RELEASED_TOO_MANY_TIMES_ERROR_MESSAGE = "The number of threads that the semaphore can release has been exceeded."
WRONG_CAPACITY_ERROR_MESSAGE = "The capacity must be non-negative."


def run_threads(threads):
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def get_threads(number_of_threads, function, args=()):
    return [Thread(target=function, args=args) for _ in range(number_of_threads)]


def create_and_run_threads(number_of_threads, function, args=()):
    run_threads(get_threads(number_of_threads, function, args))


class SemaphoreErrorsTestCase(unittest.TestCase):
    def test_wrong_initial_capacity(self):
        with self.assertRaises(ValueError) as context:
            Semaphore(-1)

        self.assertTrue(check_error_message(context, WRONG_CAPACITY_ERROR_MESSAGE))

    def test_release_after_initialization(self):
        semaphore = Semaphore(3)

        with self.assertRaises(ValueError) as context:
            semaphore.release()

        self.assertTrue(check_error_message(context, RELEASED_TOO_MANY_TIMES_ERROR_MESSAGE))

    def test_released_too_many_times_one_thread(self):
        semaphore = Semaphore()

        with self.assertRaises(ValueError) as context:
            semaphore.release()

        self.assertTrue(check_error_message(context, RELEASED_TOO_MANY_TIMES_ERROR_MESSAGE))

    def test_released_too_many_times_two_threads(self):
        semaphore = Semaphore()

        def use_semaphore():
            with semaphore:
                pass

        thread = Thread(target=use_semaphore)
        thread.start()
        thread.join()

        with self.assertRaises(ValueError) as context:
            semaphore.release()

        self.assertTrue(check_error_message(context, RELEASED_TOO_MANY_TIMES_ERROR_MESSAGE))


class SemaphoreWithoutErrorsTestCase(unittest.TestCase):
    def setUp(self):
        self.lock = Lock()
        self.count = 0

    def increment_with_acquiring(self, semaphore):
        semaphore.acquire()
        with self.lock:
            self.count += 1

    def test_simple_thread_blocking(self):
        semaphore = Semaphore(3)
        threads = get_threads(4, self.increment_with_acquiring, (semaphore,))

        run_threads(threads[:-1])

        threads[-1].start()

        time.sleep(1)

        self.assertEqual(self.count, 3)

        semaphore.release()
        threads[-1].join()

    def test_acquire_less_then_threads(self):
        semaphore = Semaphore(11)

        def use_semaphore():
            with semaphore:
                with self.lock:
                    self.count += 1

        create_and_run_threads(10, use_semaphore)

        self.assertEqual(self.count, 10)

    def test_work_after_blocking(self):
        semaphore = Semaphore(6)
        threads = get_threads(7, self.increment_with_acquiring, (semaphore,))

        run_threads(threads[:-1])

        threads[-1].start()
        semaphore.release()
        threads[-1].join()

        self.assertEqual(self.count, 7)

    def test_work_after_several_blocking(self):
        semaphore = Semaphore()
        threads = get_threads(2, self.increment_with_acquiring, (semaphore,))

        self.increment_with_acquiring(semaphore)

        threads[0].start()
        semaphore.release()
        threads[0].join()

        threads[1].start()

        time.sleep(1)

        self.assertEqual(self.count, 2)

        semaphore.release()
        threads[1].join()

    def test_binary_semaphore(self):
        number_of_increments_for_one_thread = 50_000
        semaphore = Semaphore()

        def use_semaphore():
            for _ in range(number_of_increments_for_one_thread):
                with semaphore:
                    self.count += 1

        create_and_run_threads(10, use_semaphore)

        self.assertEqual(self.count, number_of_increments_for_one_thread * 10)
