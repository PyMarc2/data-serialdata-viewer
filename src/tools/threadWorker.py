from PyQt5.QtCore import *
import sys


class WorkerSignals(QObject):
    status = pyqtSignal(str)
    finished = pyqtSignal()
    taskFailed = pyqtSignal(list)


class Worker(QRunnable):
    def __init__(self, workerFunction, *args, **kwargs):
        super(Worker, self).__init__()

        self.function = workerFunction
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs["statusSignal"] = self.signals.status

    @pyqtSlot()
    def run(self):
        try:
            self.function(*self.args, **self.kwargs)
        except Exception:
            self.signals.taskFailed.emit([sys.exc_info()])
        finally:
            self.signals.finished.emit()
