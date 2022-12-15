from . import queue
from .extension import ExtensionBaseClass
import azure.storage.queue


class QueueManager:
    def __init__(
        self,
        queue: queue.QueueClient,
        input_transformer: ExtensionBaseClass | None = None,
        output_transformer: ExtensionBaseClass | None = None,
    ):
        self.queue = queue
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

        return self.queue.peek_messages(max_messages=max_messages)


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
            message = self.list_messages(1)[0]
        else:
            message = self.queue.receive_message()

        # Transform the message
        if self.output_transformer:
            transformed_message = self.output_transformer.transform_out([message]).next()

        if preview_mode:
            print(f"PREVIEW: {message=} -> {transformed_message=}")

        if not preview_mode and delete_after:
            self.queue.delete_message(message.id, message.pop_receipt)

        return message

    def next_messages(
        self,
        count: int | None=None,
        delete_after: bool = True,
        preview_mode: bool = False,
    ):
        """Loads the next messages in the queue."""
        output_messages = self.queue.receive_messages(count)
        output = self.output_transformer.transform_many(output_messages)
        
        if delete_after:
            for message in output_messages:
                self.queue.delete_message(message.id, message.pop_receipt)

        return output

    def queue_messages(self, messages: list[str] | None = None) -> azure.storage.queue.QueueMessage:
        if self.input_transformer:
            messages = self.input_transformer.transform_in()

        print(f"adding {messages=} to {self.queue=}") 

        return [self.queue.client.send_message(content=msg) for msg in messages]


    # TODO: Add a validator for the message_transformer. This ensures that the messages_will be processed correctly.

    # TODO: Add input tranformers. This will allow the user to transform the input before it is sent to the queue.

    # TODO: Add output transformers. This will allow the user to transform the output before it is returned to the user.

    # TODO: Add in-place transformers. These will transform the message and then send it back to the queue in place.