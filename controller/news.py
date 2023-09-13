from assiatant.globe import GB
from controller.nytime import Nytime
from controller.reuter import Reuter


class News:
    def __init__(self):
        if GB["config"].get('App', 'PROJECT') == 'nytime':
            Nytime()
        else:
            Reuter()


