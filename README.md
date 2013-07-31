victims-server-openshift
========================

This repo allows you to deploy a new instance of the victims-web server on openshift.

## Running on OpenShift
### Prerequisites
1. You have a valid account with OpenShift
2. You have followed the instructions at https://www.openshift.com/get-started
3. You have *rhc* installed and ready

### Creating the app
#### One Shot Deployment
This is pretty straight forward, run the following command. The app should be deployed to ```http://victims-NAMESPACE.rhcloud.com```. See bottom for a sample output.
```sh
rhc app create victims mongodb-2.2 rockmongo-1.1 python-2.7 --from-code git://github.com/victims/victims-server-openshift.git
```
_*Note:*_ The above can be used for development purposes and will be deployed on a shared gear. This cannot be used with ```--scaling``` as _rockmongo_ cannot be scaled. If you want to deploy with scaling enabled, use:
```sh
rhc app create victims mongodb-2.2 python-2.7 --scaling --from-code git://github.com/victims/victims-server-openshift.git
```
If you'd like to merge in any upstream changes as they are available, you need to configure remote/upstream. This can be done as follows:
```sh
git remote add upstream https://github.com/victims/victims-server-openshift.git
```
#### Alternative Deployment
This can be useful if the *One Shot* option fails or if you want to configure the instance from build 1.
```sh
rhc app create victims mongodb-2.2 rockmongo-1.1 python-2.7
cd victims
git remote add upstream -m master git://github.com/victims/victims-server-openshift.git
git pull -s recursive -X theirs upstream master
# Make any configuration changes here and commit them.
git push origin master
```
### Merging upstream changes
Changes from upstream for the openshift wrapper app can be merged in and the app redeployed by executing:
```sh
git pull --rebase upstream master
git push origin master
```
_Note:_ This requires remote/usptream to be configured. (See above)
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
