# AZ Queue Manager

AZ Queue Manager is a tool to manage messages in Azure Storage Queue.

It is a command line tool that can be used to send and receive messages from a queue. It can also be used to create and delete queues.


## Getting Started
### Install AZQueueManager and Extensions
```bash
# Install the base package
pip install azqueuemanager

# Install the csv-input extension
pip install azqeueuemanager-csv # or some other extension
```

## Setup your script

If this is your input file `data.json`
```json
# data.json
[
    {"id": "msg_1", "text": "hello world"},
    {"id": "msg_2": "text": "hello universe"}
]
```
Create your script.

```python
# test.py
from azqueuemanager import QueueManager, 
from azqueuemanager-json import JSONTransformer
```
We'll come back to the extension. For now, let's define our queue_client. This is the storage queue itself.

```python
# test.py
CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=MYACCOUNT;AccountKey=MYKEY;EndpointSuffix=core.windows.net" #You'll need your own connection string
queue_name="MYQUEUENAME"

queue = StorageQueue(
    connection_string,
    queue_name,
)
```
Next we'll need to setup our extension. Every extension has a transformer. That transformer has modules for passing data into and out of the queue. The input transformer will take data and create one or more messages. The output transformer will take a message and create output for each record.

 These inputs and outputs are pretty dynamic so you will need to look at the documentation for each extension to see what the input and output looks like.

The json extension the input transformer takes `json_in_file` (or `json_data`) and (optionally) a `json_out_file`. The `transform_in` will add messages from the json content. The `transform_out` will take the messages and create a json file with all the records returned.

Let's create an instance of the JSONTransformer and pass it to the QueueManager along with our queue.

```python
# test.py

json_transform = JSONTransformer(
    json_in_file='data.json',
)

queue_manager = QueueManager(
    queue=queue
    input_transformer=json_transform,
    output_transformer=json_transform,
)
```

Now we can add or pull data to/from our Queue

### Loading Data

We pass data in using the `queue_messages` method. This will use the data processed from the `input_transformer` and add it to the storage queue.

If there is no `input_transformer` then the `queue_messages` method will take a list of messages (as `messages`) and add them to the queue.

You can look at all the messages loaded into the queue using the `list_messages` method.

```python
# test.py
# load data into the queue
queue_manager.queue_messages() 


# list the messages in the queue without popping them from the stack
queue_manager.list_messages() 

# >>> [
#    {id: 1234567890, content:"{'id': 'msg_1', 'text': 'hello world'}"},
# ...
# ]
```

### Previewing Data
You can also preview the next record. The `preview_message` method will return the next message in the queue _transformed_ without removing it from the queue.

This is designed to ensure that you're data is correct before pushing it to another service.

```python 
# test.py 

queue_manager.preview_message()

# >>> PREVIEW: message={...} -> transformed_message={'id': 'msg_1', 'text': 'hello world'}
```

### Retrieving The Data

Use `next_messages(count=n)` to retrieve `n` messages from the queue and process them with the `output_transformer`. By default messages are not deleted from the queue, but you can delete them by setting `delete_after=True` in the method. 

If you don't add a count, then it will return all the messages in the queue.

You can also process the next message ONLY by using `next_message(delete_after=True)`. This may be helpful if you want to process the messages one at a time (if the messages have different key:values that may make data more compicated).

```python
# test.py

# get messages from the queue
QueueManager.next_messages() 

# >>>
#	[
#		{"id": "msg_1", "text": "hello world"},
#		{"id": "msg_2": "text": "hello universe"}
#	]

```