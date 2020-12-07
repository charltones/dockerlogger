# set base image (host OS)
FROM python:3.8

# copy the content of the local src directory to the working directory
COPY logger.py .

# command to run on container start
CMD [ "./logger.py" ]