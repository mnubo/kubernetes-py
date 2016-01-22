class BaseModel(object):

    def __init__(self):
        self.model = dict()

    def _update_model(self):
        return self

    def get(self):
        self._update_model()
        return self.model
