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

```csv
# data.csv
name,age
John, 30
Jane, 25
```

```python
from azqueuemanager import QueueManager, StorageQueue
from azqueuemanager.extensions.csv import csv_in, csv_out

CONNECTION_STRING="MY_CONNECTION_STRING"
queue_name="MYQUEUE"

queue = StorageQueue(
    connection_string,
    queue_name,
)

queue_manager = QueueManager(
    queue=queue
    input_transformer=csv_in,
    output_transformer=csv_out,
)
```

### Loading Data (Bulk)

While some extensions can manipulate individual records, the csv extension is designed to work with batches of messages. This means that the 'bulk_input_transformer' will receive a file and create a new message for each record. 

```python
queue_manager.load_messages('data.csv') 

# >>>  2 messages loaded into MYQUEUE

queue_manager.peek_messages() # This will show the messages in the queue without popping them.

# >>> [
#    {id: 1234567890, content:{"'name': 'John', 'age': 30"}},
#    {id: 1234567890, content:{"'name': 'Jane', 'age': 25"}}
# ]
```

### Retrieving Data (Bulk)

This will retrieve all messages from the queue. It will also delete the messages from the queue. To keep the messages in the queue set the `delete_after` attribute to `False`.

```python
QueueManager.recieve_messages() # This will get the messages from the queue
# >>>  2 messages received from MYQUEUE
# {
# ids: [1234567890, 1234567890],
# content:{"""name, age 
# 'John', 30
# 'Jane', 25"""}

```

### What is a Message Transformer?
THe message Transformer is a tool that can be used to transform messages entering/exiting a queue. It can be used to work with rich json messages.

### Quick Access to Storage Queue Methods
There are a few methods that are used frequently when working with queues. These methods are available as quick access commands.
