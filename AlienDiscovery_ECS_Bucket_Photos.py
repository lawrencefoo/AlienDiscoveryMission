import boto
import os
import uuid
from flask import Flask

app = Flask(__name__)

ecs_access_key_id = ''  
ecs_secret_key = ''



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


@app.route('/')
def mainmenu():

    ## Now we will define the string first
    beginhtml =  """
    <html>
    <body>

    <center><h1><font color="white">Hi, I'm Lawrence Foo:<br/>
    </br>
    """

    endhtml = """
    </center>
    </body>
    </html>
    """

    photoshtml = ""
    for k in b.list():
        photoecs = "http://131608195099923191.public.ecstestdrive.com/" +bname +"/" + k.key
        print photoecs
        photoshtml = photoshtml + """<img src="http://131608195099923191.public.ecstestdrive.com/{}/{}"><br>""".format(bname, k.key)
        print photoshtml
    ## And then we return it. This gives us more flexibility
    ## than building it just-in-time for the "return" function

    response = beginhtml + photoshtml + endhtml
    return response


#### Get an existing key
#k = b.get_key(filename)

#### Get specific metata for a key
#print k.get_metadata('vmax')
####The metadata can be seen in S3 in the "http headers" tab
####It gets stored as "x-amz-meta-vmax"

#### Delete an existing key
#k = b.get_key(filename)
#k.delete()

#### Get all buckets for a given session
#print session.get_all_buckets()

#### Get all keys for a given bucket
#print b.get_all_keys()

extenstion = ".jpg"
#### Display all keys in all buckets
#for bucket in session.get_all_buckets():
#    print "In bucket: " + bucket.name
#    for object in bucket.list():
#        if (str(object.key).endswith(extenstion) == 1): 
#            print(object.key)

#### Display specific metadata for all keys in a bucket
#for k in b.list():
#    print k.key
#    key = b.get_key(k)
#    print key.get_metadata('vmax')
    
if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
