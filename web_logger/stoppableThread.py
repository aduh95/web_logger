from threading import Event, Thread


class StoppableThread(Thread):
    def __init__(self, stop_event: Event = None):
        Thread.__init__(self)
        if stop_event:
            StopThreadOnEvent(self, stop_event).start()

    def stop(self):
        raise NotImplementedError()


class StopThreadOnEvent(Thread):
    def __init__(self, stoppable_thread: Thread, stop_event: Event):
        Thread.__init__(self)
        self.stoppable_thread = stoppable_thread
        self.stop_event = stop_event

    def run(self):
        self.stop_event.wait()
        self.stoppable_thread.stop()
