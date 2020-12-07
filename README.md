Steps:

# try the file locally first - I ran all this on a Cloud9 machine
./logger.py
# you should be able to curl localhost:8080

# build a docker container
docker build -t logtest .

# test the docker container locally
docker run -p 8080:8080 logtest
# you should be able to curl localhost:8080

# check the docker image is there
docker images

# create an ECR repo
aws ecr create-repository --repository-name logtest

# command line login foo for ECR
aws ecr get-login --no-include-email

# <run the output of the last command>

# tag image to your ECR repo
docker tag logtest <account>.dkr.ecr.eu-west-1.amazonaws.com/logtest

# push image up - do this every time you change it
docker push <account>.dkr.ecr.eu-west-1.amazonaws.com/logtest

# check image is there
aws ecr describe-images --repository-name logtest

# create an ECS cluster
aws ecs create-cluster --cluster-name logtest  

# find AMI ID of ECS ready AMI
aws ssm get-parameters --names /aws/service/ecs/optimized-ami/amazon-linux/recommended

# start an EC2 instance (you will need to edit this script)
./launch-instance.sh
<wait for it to join cluster>

# register task defn with ECS (need to edit the file too)
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# create the log group in CWL
<create the log group>

# start the ECS task - takes a few seconds to come up
aws ecs run-task --cluster arn:aws:ecs:eu-west-1:<account>:cluster/logtest --task-definition arn:aws:ecs:eu-west-1:<account>:task-definition/logtest-task:1 <-- the number depends on the version of task defn

# you should be able to ssh into the ECS instance machine, once there this will show you connections made - one will be to CWL
sudo netstat -t

# iptables can cut the connections to CWL. Adding an entry to /etc/hosts for:
52.95.125.162	logs.eu-west-1.amazonaws.com
# will stop you having to block more IPs
sudo iptables -A OUTPUT -p tcp -d <ip> --dport 443 -j DROP

# to undo the iptables work, use this to view the rules
sudo iptables -L --line-numbers

# and this to drop by number
sudo iptables -D OUTPUT 1

ab -n 1000 http://<ip>:8080/