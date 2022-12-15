import os
from azqueuemanager.queue import QueueClient
from azqueuemanager import QueueManager
from extensions.json_parser import JSONTransformer

json_parser = JSONTransformer(
    parse_array=True,
    json_file='test_json_in.json',
    )

queue_client = QueueClient.from_connection_string(
    queue_name = 'test-queue',
)

queue_mgr = QueueManager(
    queue = queue_client,
    input_transformer= json_parser,
    output_transformer= json_parser,
)

if __name__ == '__main__':
    print("loading")
    queue_mgr.queue_messages()
    print("loaded")