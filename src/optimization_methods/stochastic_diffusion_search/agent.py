class Agent:
    def __init__(self, hyp, is_active):
        self._hyp = hyp
        self._is_active = is_active

        self._score = 0

    @property
    def hyp(self):
        return self._hyp

    @hyp.setter
    def hyp(self, value):
        self._hyp = value

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
