import logging
import os
import typing

import azure.storage.queue



class QueueClient:
    def __init__(
        self,
        *,
        client: azure.storage.queue.QueueClient,
        queue_name: str,
    ):
        self.client = client
        self.queue_name = queue_name

    def __repr__(self):
        return str(self)

    def is_exists(self):
        try:
            self.client.get_queue_properties()
            return True
        except:
            return False

    @classmethod
    def ConnectionStringAuth(cls):
        """Auth object for using a connection string to authenticate with Azure Storage."""
        def __init__(
            self, *, connection_string: typing.Optional[str] = None, queue_name: str
        ):

            if connection_string is None:
                connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")

                if connection_string is None:
                    logging.warning(
                    "connection_string not passed or in AZURE_STORAGE_CONNECTION_STRING environment variable."
                    )

            client = azure.storage.queue.QueueClient.from_connection_string(
                connection_string,
                queue_name
            )

            return cls(client=client, queue_name=queue_name)

    @property
    def connection_string(self):
        """You should not be able to get the connection string directly from the auth object. This is a security risk."""
        raise ValueError(
            'Connection String Cannot be retrieved from ConnectionStringAuth.\n \
            Please check your environment variables or https://portal.azure.com'
        )

    def __str__(self):
        return f"Auth(connection_string={self.connection_string}, queue_name={self.queue_name})"


# TODO: Create other Auth Types: Currently only Connection String is supported