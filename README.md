victims-server-openshift
========================

This repo allows you to deploy a new instance of the victims-web server on openshift.

## Running on OpenShift
### Prerequisites
1. You have a valid account with OpenShift https://www.openshift.com/get-started
2. You have the s2i tool installed locally https://github.com/openshift/source-to-image

### Log in to Openshift
```sh
oc login https://console.starter-us-east-1.openshift.com
```

### Create a new project
```sh
oc new-project victims
```

### (Optional) Deploy a database
It's recommended to use a MongoDB database hosted outside of Openshift. However for development purposes a temporary database can provisionsed inside Openshift using the provided template:
```sh
oc process -f mongodb-ephemeral.yaml | oc create -f -
```
*Due to the authentication mechanism being updated to SCRAM-SHA1 in Mongo 3.x, we have a requirement to use an earlier version of MongoDB, eg. 2.6*
*The emphemeral template doesn't use permanent storage with a persistent volume, all data will be lost when the pod is migrated!*

### Build the victims-web image with s2i tool
```sh
s2i build -c . centos/python-27-centos7 registry.starter-us-east-1.openshift.com/victims/victims-web
```
*The ''-c' argument tells s2i to use the local copy, not one stored in the local git repository*

### Test the build image
It's now possible to run the image locally to test any changes:
```sh
docker run -it registry.starter-us-east-1.openshift.com/victims/victims-web
```

### Push the image into Openshift
You'll need to login to the openshift docker registry using your token. The token can be obtained by first logging into Openshift:
```sh
oc login https://console.starter-us-east-1.openshift.com
```

Then obtain your token like so:
```sh
oc whoami -t
```

Then login to the docker registry:
```sh
docker login -u <openshift-username> -p <token> registry.starter-us-east-1.openshift.com
```

Push the build image to the registry:

```sh
sudo docker push registry.starter-us-east-1.openshift.com/victims/victims-web
```

### Create the app using image
```sh
oc new-app -e MONGODB_DB_HOST=mongodb.victims.svc victims-web --name=web
```

### Importing data
1. Get the app's SSH address by running ```rhc app show victims```
2. SSH into the server.
3. Download the data file you want to import to ```$OPENSHIFT_DATA_DIR```
4. Run the following command replacing ```$INPUTFILE``` with your file name.

```sh
mongoimport -d $OPENSHIFT_APP_NAME -c hashes --type json --file $OPENSHIFT_DATA_DIR/$INPUTFILE  -h $OPENSHIFT_MONGODB_DB_HOST  -u admin -p $OPENSHIFT_MONGODB_DB_PASSWORD --port $OPENSHIFT_MONGODB_DB_PORT
```
### Configuring the deploytment
#### Application Configuration
Any application configuration can be pushed by changing the ```configs/victimsweb.cfg``` file in the repo. This will be used instead of the ```application.cfg``` provided by victims-web.
Alternatively, a file ```$OPENSHIFT_DATA_DIR/victimsweb.cfg``` can be created so that the application uses this instead of ```configs/victimsweb.cfg```.
#### Build Hook Configuration
We use ```configs/victimsweb.build.env``` file for doing a few build time tricks. This file is sourced before a the build hook executes.

1. Branches/Tags: You can specify this as ```VICTIMS_GIT_BRANCH=master```. By default the master branch is checked out and used.
2. Specify your fork: This can be done by setting ```VICTIMS_GIT_URL``` to your repository url. This will delete any existing checkout.
3. Clean checkout: You can request this by setting ```VICTIMS_GIT_CLEAN=0``` to ```1```.

#### HA-Proxy Configuration
*Stop haproxy from dropping client connections*
```diff
    option http-server-close
+    option http-pretend-keepalive
```
*Forward client IP address*
```diff
-    #option forwardfor       except 127.0.0.0/8
+    option forwardfor       except 127.0.0.0/8
```
*Enable authentication on status page. Be sure to replace the password.*
```diff
listen stats $IP:$PORT
    mode http
    stats enable
    stats uri /
+    stats realm HAProxy\ Statistics
+    stats auth admin:replacethispassword
```
*Add cookie config so that haproxy routes requests to the correct gear.*
```diff
listen express $IP:$PORT
+    cookie GEAR insert indirect nocache
    option httpchk GET /
    balance leastconn
    server  filler $IP:$PORT backup
```
*If running a development/testing environment or if you only have one node, it might be useful to remove the heart-beat checks.*
```diff
listen express $IP:$PORT
    cookie GEAR insert indirect nocache
-    option httpchk GET /
    balance leastconn
    server  filler $IP:$PORT backup
```

### Sample creation output
```sh
$ rhc app create victims mongodb-2.2 python-2.7 --from-code git://github.com/victims/victims-server-openshift.git
Application Options
-------------------
  Namespace:   abn
  Cartridges:  mongodb-2.2, python-2.7
  Source Code: git://github.com/victims/victims-server-openshift.git
  Gear Size:   default
  Scaling:     no

Creating application 'victims' ... done

Waiting for your DNS name to be available ... done

Downloading the application Git repository ...
Cloning into 'victims'...
Warning: Permanently added the RSA host key for IP address '**.***.***.**' to the list of known hosts.

Your application code is now in 'victims'

victims @ http://victims-abn.rhcloud.com/ (uuid: **********************)
--------------------------------------------------------------------------
  Created:         7:33 PM
  Gears:           1 (defaults to small)
  Git URL:         ssh://$UID@victims-abn.rhcloud.com/~/git/victims.git/
  Initial Git URL: git://github.com/victims/victims-server-openshift.git
  SSH:             $UID@victims-abn.rhcloud.com

  python-2.7 (Python 2.7)
  -----------------------
    Gears: Located with mongodb-2.2

  mongodb-2.2 (MongoDB NoSQL Database 2.2)
  ----------------------------------------
    Gears:          Located with python-2.7
    Connection URL: mongodb://$OPENSHIFT_MONGODB_DB_HOST:$OPENSHIFT_MONGODB_DB_PORT/
    Database Name:  victims
    Password:       ***********
    Username:       admin

RESULT:
Application victims was created.
MongoDB 2.2 database added.  Please make note of these credentials:
   Root User:     admin
   Root Password: ***********
   Database Name: victims
Connection URL: mongodb://$OPENSHIFT_MONGODB_DB_HOST:$OPENSHIFT_MONGODB_DB_PORT/

```
