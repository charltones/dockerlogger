Steps:

_try the file locally first - I ran all this on a Cloud9 machine_

`./logger.py`

_you should be able to:_
`curl localhost:8080`

_build a docker container_

`docker build -t logtest .`

_test the docker container locally_

`docker run -p 8080:8080 logtest`

_you should be able to:_
`curl localhost:8080`

_check the docker image is there_

`docker images`

_create an ECR repo_

`aws ecr create-repository --repository-name logtest`

_command line login foo for ECR_

`aws ecr get-login --no-include-email`

_<run the output of the last command>_

_tag image to your ECR repo_

`docker tag logtest <account>.dkr.ecr.eu-west-1.amazonaws.com/logtest`

_push image up - do this every time you change it_

`docker push <account>.dkr.ecr.eu-west-1.amazonaws.com/logtest`

_check image is there_

`aws ecr describe-images --repository-name logtest`

_create an ECS cluster_

`aws ecs create-cluster --cluster-name logtest`

_find AMI ID of ECS ready AMI_

`aws ssm get-parameters --names /aws/service/ecs/optimized-ami/amazon-linux/recommended`

_start an EC2 instance (you will need to edit this script)_

`./launch-instance.sh`

_<wait for it to join cluster>_

_register task defn with ECS (need to edit the file too)_

`aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json`

_create the log group in CWL_
_<create the log group>_

_start the ECS task - takes a few seconds to come up_

`aws ecs run-task --cluster arn:aws:ecs:eu-west-1:<account>:cluster/logtest --task-definition arn:aws:ecs:eu-west-1:<account>:task-definition/logtest-task:1`

_the trailing number depends on the version of task defn_

_you should be able to ssh into the ECS instance machine, once there this will show you connections made - one will be to CWL_

`sudo netstat -t`

_iptables can cut the connections to CWL. Adding an entry to /etc/hosts for:_

`52.95.125.162	logs.eu-west-1.amazonaws.com`

_will stop you having to block more IPs. Run it like this:_

`sudo iptables -A OUTPUT -p tcp -d <ip> --dport 443 -j DROP`

_to undo the iptables work, use this to view the rules_

`sudo iptables -L --line-numbers`

_and this to drop by number_

`sudo iptables -D OUTPUT 1`

_Use ab to throw some traffic at the server_

`ab -n 1000 http://<ip>:8080/`
