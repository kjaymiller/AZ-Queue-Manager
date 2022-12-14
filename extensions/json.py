import json


class JSONTransformer:
    """This class transforms json data into a format that can be used by the queue."""

    parse_array: bool # If true, the data will be parsed as an array of objects.

    def __init__(self, parse_array: bool = False):
        self.parse_array = parse_array

    def transform_in(self, filepath: Path | str):
        """This method transforms the data into a format that can be used by the queue."""
        with open(filepath, "rb") as file:
            data = json.load(file) 

        if self.parse_array:
            for item in data:
                yield json.dumps(item)
        else:
            yield data

    def transform_one(self, data: str):
        return json.loads(data)

    def transform_many(self, data: list[str]):
        for item in json.loads(data):
            yield item