#this sample illustrates fundamentals of how to use Azure to create, read and delete files within Blob Storage

#first we import Azure.Storage modules (and the OS module for IO)
from azure.storage import *
import os

#put your account name and key here
account = 'youracct'
key = 's/r13BjGwGmkbsJ2GqWt5YaI4UC5ou51UDdq8mTv6foULNVl1pC/C6ijQiI3ziuJGfSUA03zrSsLx1tTkU0d9g=='

#get a handle to your account
table_service = TableService(account_name=account, account_key=key)
# this won't report if it fails so it's safe to execute
table_service.delete_table('auditrecord')
# create an audit record entity based on collecting information on applications
# use the PartitionKey as the data centre name and RowKey as a simple index
table_service.create_table('auditrecord')
# first entity is an error entity
entity1 = Entity()
entity1.PartitionKey = 'North Europe'
entity1.RowKey = '1'
entity1.description = 'Application failed to connect to server'
entity1.type = 'error'
# second entity is an info entity
entity2 = Entity()
entity2.PartitionKey = 'East US 2'
entity2.RowKey = '2'
entity2.description = 'Successful user authentication'
entity2.type = 'information'
# add in additional column to show schemaless dynamic nature
entity2.attempts = '1'
# add the entities to the table service
table_service.insert_entity('auditrecord', entity1)
# show this in a REPL or debug to show the schema changes and the null value being passed to the previous entity
table_service.insert_entity('auditrecord', entity2)

# show an update of an entity
entity2.attempts = '2'
table_service.update_entity('auditrecord', 'East US 2', '2', entity2)

# get the entity details back
records = table_service.query_entities('auditrecord', "PartitionKey eq 'North Europe' or PartitionKey eq 'East US 2'", 'description')
for record in records:
    print(record.description)