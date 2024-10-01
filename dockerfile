FROM ubuntu:22.04

ENV TZ="Asia/Kolkata"
RUN date


# Set timezone:
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone

# Update and install the necessary packages
RUN apt update -y && apt upgrade -y && apt install -y python3 python3-pip python3-venv git python3-full

# Create the python virtual environment
RUN python3 -m venv /rero/iot_bot/venv
RUN . /rero/iot_bot/venv/bin/activate


# Install requirements
# Despite the use of volume, this is required as volumes are set up towards the end of the container setup
COPY ./requirements.txt /rero/iot_bot/venv/requirements.txt
RUN python3 -m pip install -r /rero/iot_bot/venv/requirements.txt

# Volume for the source
RUN mkdir -p /rero/iot_bot/app
VOLUME ["/rero/iot_bot/app"]

# IoT Bot communication port
EXPOSE 8082

# CMD [ "/bin/bash" ]
CMD ["/bin/bash", "/rero/iot_bot/app/startup_dev.sh"]