class _WithStr:
    def __init__(self, call, string):
        self._call = call
        self._string = string

    @property
    def __call__(self):
        return self._call

    @property
    def __repr__(self):
        return self._call.__repr__

    def __str__(self):
        return self._string
