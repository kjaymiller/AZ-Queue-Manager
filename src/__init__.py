import typing
from typing import Callable

from . import storage, twitter
import azure.storage.queue


class QueueManager:
    def __init__(self, storage_auth: storage.Auth):
        self.queue = storage_auth.Client

    def list_messages(
        max_messages: int | None = None
    ):
        """
        Returns a list of the messages in the queue without modifying the queue.

        This is a wrapper for azure.storage.queue.QueueClient.peek_messages
        """

        return self.queue.peek_messages(max_messages=max)



    def send_next_message(
        self,
        message_transformer: typing.Optional[Callable[[str], dict]] = lambda message: {
            "text": message
        },
        delete_after: typing.Optional[bool] = True,
        preview_mode: typing.Optional[bool] = False,
    ):
        if preview_mode:
            next_message = self.queue.peek_messages()[0]
        else:
            next_message = self.queue.receive_message()

        # Turns queue message into tweet arguments
        # Must be a dict containing arguments from
        # https://docs.tweepy.org/en/stable/client.html#tweepy.Client.create_tweet
        # Or "file" (byte array)/"filename" (str) to be uploaded w/Twitter API v1
        tweet_args = message_transformer(next_message["content"])

        if (file := tweet_args.get("file")) and (
            filename := tweet_args.get("filename")
        ):
            if preview_mode:
                print(f"The {filename} file with contents {file} would get uploaded.")
                tweet_args["media_ids"] = ["UPLOADED-ID"]
            else:
                media = self.twitterv1.media_upload(file=file, filename=filename)
                tweet_args["media_ids"] = [media.media_id]
            del tweet_args["file"]
            del tweet_args["filename"]

        # Send the tweet
        if preview_mode:
            print(f"This would send tweet with {tweet_args}")
        else:
            self.twitterv2.create_tweet(**tweet_args)

        # Delete from queue if desired
        if not preview_mode and delete_after:
            self.queue.delete_message(next_message.id, next_message.pop_receipt)

    def queue_message(self, message: str|json, message_transformer) -> azure.storage.queue.QueueMessage
        self.queue.send_message(message)


    # TODO: Add a validator for the message_transformer. This ensures that the messages_will be processed correctly.

    # TODO: Add input tranformers. This will allow the user to transform the input before it is sent to the queue.

    # TODO: Add output transformers. This will allow the user to transform the output before it is returned to the user.

    # TODO: Add in-place transformers. These will transform the message and then send it back to the queue in place.