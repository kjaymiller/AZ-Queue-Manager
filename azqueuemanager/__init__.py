from . import queue
from .extension import ExtensionBaseClass
import azure.storage.queue
import azure.functions


class QueueManager:
    def __init__(
        self,
        queue: queue.QueueClient,
        has_queue_trigger: bool = False,
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

        return self.queue.client.peek_messages(max_messages=max_messages)

    def preview_message(
        self,
    ) -> str:
        """
        Returns the next message in the queue without modifying the queue.
        """

        message = self.list_messages(1)[0]
        print(message)

        if self.output_transformer:
            transformed_message = self.output_transformer.transform_preview(message)
            
        else:
            transformed_message = message.content

        return f"PREVIEW: {message=} -> {transformed_message=}"

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
        message = self.queue.client.receive_message()

        # Transform the message
        self.transform_message(message)

        if not preview_mode and delete_after:
            self.queue.client.delete_message(message.id, message.pop_receipt)

        return message

    def next_messages(
        self,
        count: int | None=None,
        delete_after: bool = True,
    ):
        """Loads the next messages in the queue."""
        output_messages = self.queue.client.receive_messages(max_messages=count)
        if self.output_transformer:
            output = self.output_transformer.transform_out(output_messages)
        
        else:
            output = output_messages
        
        if delete_after:
            for message in output_messages:
                self.queue.client.delete_message(message.id, message.pop_receipt)

        return output

    def queue_messages(self, messages: list[str] | None = None) -> azure.storage.queue.QueueMessage:
        """
        enqueue the messages into the queue_client.
        If there is a transformer, transform using the `transform_in` method for the extensions
        """

        if self.input_transformer:
            messages = self.input_transformer.transform_in()

        return [self.queue.client.send_message(content=msg) for msg in messages]


    def transform_message(self, message: azure.functions.QueueMessage) -> any:
        logging.info(f"Transforming message {message=}")
        if self.output_transformer:
            return self.output_transformer.transform_out([message.get_body().decode('utf-8')]).next()

        logging.info("No Output Transformer. Returning message %s", message)
        return message

    # TODO: Add a validator for the message_transformer. This ensures that the messages_will be processed correctly.

    # TODO: Add input tranformers. This will allow the user to transform the input before it is sent to the queue.

    # TODO: Add output transformers. This will allow the user to transform the output before it is returned to the user.

    # TODO: Add in-place transformers. These will transform the message and then send it back to the queue in place.