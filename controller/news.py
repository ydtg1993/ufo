from assiatant import GB
from controller.nytime import Nytime
from controller.reuter import Reuter


class News:
    def __init__(self):
        Nytime()
        Reuter()
