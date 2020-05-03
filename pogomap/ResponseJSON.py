import inspect

import simplejson
import flask

class ResponseJSON(flask.Response):
    default_mimetype = "application/json"

    def __init__(self, payload=None, payload_name="payload", error=None, exception=None):
        self.payload = payload
        self.payload_name = payload_name
        self.error = error
        self.exception = exception

        super(ResponseJSON, self).__init__(response=self.to_json())

    def to_obj(self):
        obj = {}

        if self.error is not None:
            obj["done"] = False
            obj["error"] = self.error
        elif self.exception is not None:
            obj["done"] = False
            obj["error"] = type(self.exception).__name__
        else:
            obj["done"] = True
            if self.payload is not None:
                if inspect.isgenerator(self.payload):
                    self.payload = list(self.payload)

                obj[self.payload_name] = self.payload

        return obj

    def to_json(self):
        return simplejson.dumps(self.to_obj(), default=lambda obj: obj.__dict__)
