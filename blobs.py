#this sample illustrates fundamentals of how to use Azure to create, read and delete files within Blob Storage

#first we import Azure.Storage modules (and the OS module for IO)
from azure.storage import *
import os

#put your account name and key here
account = 'wenmingipython'
key = 's/r13BjGwGmkbsJ2GqWg5YaI8UC8ou51UDdq8mTv6foULNVl1pC/C6ijQiI3ziuJGfSUA03zrSsLx1tTkU0d9g=='

open(r'sample.txt', 'w').write(r'some text!!')

#get a handle to your account
blob_service = BlobService(account_name=account, account_key=key)

#create a container if it doesnt already exist
blob_service.create_container('testcontainer')

#put a blob into a container
myblob = open(r'sample.txt', 'r').read()
blob_service.put_blob('testcontainer', 'myblob', myblob, x_ms_blob_type='BlockBlob')

#list all blobs in a container
blobs = blob_service.list_blobs('testcontainer')
for blob in blobs:
    print(blob.name)
    print(blob.url)

#download the blob locally
downloadedblob = blob_service.get_blob('testcontainer', 'myblob')
with open(r'downloadedfile.txt', 'w') as f:
    f.write(downloadedblob)

#delete the file locally
os.remove(r'downloadedfile.txt')

#delete the blob remotely
for blob in blobs:
    blob_service.delete_blob('testcontainer', 'myblob')

# cleanup and delete the container
blob_service.delete_container('testcontainer')