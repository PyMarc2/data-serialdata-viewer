import numpy as np
import time

EIGHTBITS = 0
PARITY_NONE = 0
STOPBITS_ONE = 0


class Serial:

    def __init__(self, port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE,
                 timeout=None, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None,
                 exclusive=None, **kwargs):

        self.is_open = False
        self.portstr = None
        self.name = None
        # correct values are assigned below through properties
        self._port = None
        self._baudrate = None
        self._bytesize = None
        self._parity = None
        self._stopbits = None
        self._timeout = None
        self._write_timeout = None
        self._xonxoff = None
        self._rtscts = None
        self._dsrdtr = None
        self._inter_byte_timeout = None
        self._rs485_mode = None  # disabled by default
        self._rts_state = True
        self._dtr_state = True
        self._break_state = False
        self._exclusive = None

        # assign values using get/set methods using the properties feature
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.write_timeout = write_timeout
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.dsrdtr = dsrdtr
        self.inter_byte_timeout = inter_byte_timeout
        self.exclusive = exclusive

        # watch for backward compatible kwargs
        if 'writeTimeout' in kwargs:
            self.write_timeout = kwargs.pop('writeTimeout')
        if 'interCharTimeout' in kwargs:
            self.inter_byte_timeout = kwargs.pop('interCharTimeout')
        if kwargs:
            raise ValueError('unexpected keyword arguments: {!r}'.format(kwargs))

        if port is not None:
            self.open()

    def open(self):
        self.open = 1

    def read(self):
        if self.open:
            time.sleep(1 / self.baudrate)
            return np.random.rand(1)[0]
        else:
            pass

    def close(self):
        self.open = 0
