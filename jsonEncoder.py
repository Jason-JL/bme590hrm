import json
import numpy


class NumpyAwareJSONEncoder(json.JSONEncoder):
    """
    override JsonEncoder to deal with numpy.darray
    """
    def default(self, obj):
        if isinstance(obj, numpy.ndarray) and obj.ndim == 1:
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)