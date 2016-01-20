from kubernetes.models.v1.BaseModel import BaseModel


class DeleteOptions(BaseModel):
    def __init__(self, kind, grace_period_seconds=30, model=None):
        BaseModel.__init__(self)
        if model is not None:
            assert isinstance(model, dict)
            self.model = model
        else:
            if kind is None or not isinstance(kind, str):
                raise SyntaxError('kind must be a string')
            self.model = dict(kind=kind, apiVersion='v1', gracePeriodSeconds=grace_period_seconds)

    def set_grace_period_seconds(self, period=None):
        if period is None or not isinstance(period, int):
            raise SyntaxError('period must be a positive integer')
        self.model['gracePeriodSeconds'] = int(period)
        return self
