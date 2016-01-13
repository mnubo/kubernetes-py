class DeleteOptions:
    def __init__(self, kind, grace_period_seconds=30):
        if kind is None or not isinstance(kind, str):
            raise SyntaxError('kind must be a string')
        self.model = dict(kind=kind, apiVersion='v1', gracePeriodSeconds=grace_period_seconds)

    def get(self):
        return self.model

    def set_grace_period_seconds(self, period=None):
        if period is None or not isinstance(period, int):
            raise SyntaxError('period must be a positive integer')
        self.model['gracePeriodSeconds'] = int(period)
        return
