import sys

class Tee(object):
    def __init__(self, name, mode):
        self._file = open(name, mode)
        self._stdout = sys.stdout
        sys.stdout = self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        if self._file is None:
            return
        sys.stdout = self._stdout
        self._file.close()
        self._stdout = None
        self._file = None

    def write(self, data):
        self._file.write(data)
        self._stdout.write(data)
