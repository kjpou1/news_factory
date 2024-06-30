import json
from datetime import datetime, time

import pandas as pd


class DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (pd.Timestamp, datetime)):
            return o.isoformat()
        elif isinstance(o, time):
            return o.strftime('%H:%M:%S')
        return super().default(o)
