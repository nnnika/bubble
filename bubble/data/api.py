

class DataApi(object):

    def __init__(self):
        pass

    def get(self, table, code, start, end, fields):
        return getattr(self, table)(code, start, end, fields)

    def get_factor(self, table, code, start, end):

        return {
            "000001.SH": {"date": ['2021-01-05', ], "value": [3600, ]}
        }