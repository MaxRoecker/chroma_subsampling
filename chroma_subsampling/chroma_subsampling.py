import numpy as np


class ChromaSubsampler(object):
    def __init__(self, a, b, J=4):
        super(ChromaSubsampler, self).__init__()
        self._J = J
        if a == 4 and b == 4:
            (col_step, row_step) = (1, 1)
        elif a == 4 and b == 0:
            (col_step, row_step) = (1, 2)
        elif a == 2 and b == 2:
            (col_step, row_step) = (2, 1)
        elif a == 2 and b == 0:
            (col_step, row_step) = (2, 2)
        elif a == 1 and b == 1:
            (col_step, row_step) = (4, 1)
        elif a == 1 and b == 0:
            (col_step, row_step) = (4, 2)
        else:
            raise ValueError('Invalid value for argument "a" or "b"')
        self._col_step = col_step
        self._row_step = row_step

    def encode(self, image):
        encoded = image[::self._col_step, ::self._row_step]
        return encoded

    def decode(self, encoded):
        decoded_0 = np.repeat(encoded, self._col_step, axis=0)
        decoded = np.repeat(decoded_0, self._row_step, axis=1)
        return decoded
