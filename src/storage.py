import logging
import os
import typing

import azure.storage.queue


class Auth:
    def __init__(
        self, *, connection_string: typing.Optional[str] = None, queue_name: str
    ):
        if connection_string is None:
            connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
            if connection_string is None:
                logging.warning(
                    "connection_string not passed or in AZURE_STORAGE_CONNECTION_STRING environment variable."
                )
        self.connection_string = connection_string
        self.queue_name = queue_name

    @property
    def Client(self) -> azure.storage.queue.QueueClient:
        return azure.storage.queue.QueueClient.from_connection_string(
            self.connection_string, self.queue_name
        )
