#!/bin/bash

aws ec2 run-instances --image-id ami-<the id> --count 1 --instance-type t2.medium \
 --key-name <your key> --security-group-ids <sg> \
 --subnet-id <subnet> --iam-instance-profile Name=<Role> \
 --user-data file://userdata.txt \
 --tag-specifications "ResourceType=instance,Tags=[{Key=Name, Value=logtest}]"