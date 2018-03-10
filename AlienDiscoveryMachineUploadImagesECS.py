import boto
import os
import uuid
#from flask import Flask
#app = Flask(__name__)

ecs_access_key_id = '##############@ecstestdrive.emc.com'  
ecs_secret_key = '##########################'



#### This is the ECS syntax. It requires "host" parameter
session = boto.connect_s3(ecs_access_key_id, ecs_secret_key, host='object.ecstestdrive.com')  
bname = 'aliendiscovery'

#### Get bucket and display details
b = session.get_bucket(bname)
print "ECS connection is: " + str(session)
print "Bucket is: " + str(b)

filename = ""

#### Create new key, define metadata, upload and ACL
for each_photo in os.listdir("uploadimg"):
    print "Uploading " + str(each_photo)
    filename = each_photo
    src = os.path.join("uploadimg", each_photo)
    print "full path to photo is : " + src
    k = b.new_key(filename)
    k.set_metadata('moon', 'yes') 
    k.set_contents_from_filename(src)
    k.set_acl('public-read')

print "Finish Upload Images To ECS"
