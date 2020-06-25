import threading
import atexit


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def start(self):
        super().start()
        atexit.register(self.stop)

    def stop(self):
        self._stop_event.set()
        atexit.unregister(self.stop)

    @property
    def stopped(self):
        return self._stop_event.is_set()