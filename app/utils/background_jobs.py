from concurrent.futures import ThreadPoolExecutor
import threading


class BackgroundJobRunner:
    def __init__(self, max_workers=2):
        self._executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="attendance-bg")
        self._active_jobs = 0
        self._lock = threading.Lock()

    def submit(self, func, *args, **kwargs):
        with self._lock:
            self._active_jobs += 1

        future = self._executor.submit(func, *args, **kwargs)

        def _cleanup(_future):
            with self._lock:
                self._active_jobs = max(0, self._active_jobs - 1)

        future.add_done_callback(_cleanup)
        return future

    def describe(self):
        return {"active_jobs": self._active_jobs}


background_jobs = BackgroundJobRunner()
