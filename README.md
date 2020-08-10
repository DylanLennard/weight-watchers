# Weight Watchers

## Overview
During covid, it's become increasingly difficult to find weight lifting bumper plates available for sale. In particular, I keep finding the Ethos bumper plates at Dick's sporting goods store are always unavailable. While they have the 'notify me when available' by email available, I was more interested in receiving a text message with a link to buy the actual item online.

Thus I made a fun little program to query for 25, 35, and 45 pound plates which will email me via text message when available (checking roughly every 20 minutes).

The purpose of this was to be a fun little saturday night project which would result in the following
* me playing around with SNS being subscribed to by a mobile number
* to finally purchase some more weight!

## How it Works
This program will take a json file of URLs for different size weight plates and
* hits the URL for that particular weight plate
* scans the HTML for the 'ship to me' availability message on the item
* if the item is available, it sends an SNS message with a link to buy the item


## How to set this up yourself
* make sure you have creds on aws all setup
* create an sns topic
* subscribe your mobile number to this topic
* install [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtual](https://github.com/pyenv/pyenv-virtualenv)
* install [docker](https://docs.docker.com/get-docker/)
* install [sam-cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* To run locally, run the following
```BASH
# setup the virtualenv
make create_env
make activate_env
make install_reqs
```

In order for this to run successfully, you'll need to
* make sure aws configure has been run locally
* to actually run the sns commands, set QA=False and SNS_TOPIC={your sns topic arn}

Once that's setup, run the following to actually execute the function locally
```BASH
make build # build the executable
make run
make clean # when done
```

### Setting Up With Lambda
The above sets things up for running this locally. To setup on lambda:
* create a lambda function
* upload the zip file created from `make build`
* set env vars in lambda
* adjust timeout to at least 10 seconds
* set an eventbuilder trigger with a cron task of the frequency you want the script to run
