from typing import Callable

from . import storage, twitter
import azure.storage.queue


class QueueManager:
    def __init__(
        self,
        storage_auth: storage.Auth,
        input_transformer: Callable[...]|None = None,
        output_transformer: Callable[...]| None = None,
        self.queue = storage_auth.Client
    )
        self.input_transformer = input_transformer
        self.output_transformer = output_transformer

    def __repr__(self):
        return f"QueueManager({self.queue=})"

    def list_messages(
        self,
        max_messages: int | None = None
    ):
        """
        Returns a list of the messages in the queue without modifying the queue.

        This is a wrapper for azure.storage.queue.QueueClient.peek_messages
        """

        return self.queue.peek_messages(max_messages=max)


    def next_message(
        self,
        delete_after: bool = True,
        preview_mode: bool = False,
    ) -> azure.storage.queue.QueueMessage:
        """
        Loads the next message in the queue.
        The message_transformer is a function that takes the message and returns a dict of arguments for the tweet.
        If preview_mode is True, the message will be peeked and the deque_count will not change.
        If delere_after is True, the message will be deleted after it is processed.
        """
        if preview_mode:
            message = self.list_messages()[0]
        else:
            message = self.queue.receive_message()

        # Transform the message
        if self.output_transformer:
            transformed_message = self.output_transformaer.transform_one(message["content"])

        if preview_mode:
            print(f"PREVIEW: {message=} -> {transformed_message=}")

        if not preview_mode and delete_after:
            self.queue.delete_message(message.id, message.pop_receipt)

        return message

    def next_messages(
        count: int | None=None,
        delete_after: bool = True,
    ):
        """Loads the next messages in the queue."""
        for message in self.recieve_messages(max_messages=count):

    def queue_message(self, message: str|dict[any, any], message_transformer) -> azure.storage.queue.QueueMessage
        self.queue.send_message(message)


    # TODO: Add a validator for the message_transformer. This ensures that the messages_will be processed correctly.

    # TODO: Add input tranformers. This will allow the user to transform the input before it is sent to the queue.

    # TODO: Add output transformers. This will allow the user to transform the output before it is returned to the user.

    # TODO: Add in-place transformers. These will transform the message and then send it back to the queue in place.