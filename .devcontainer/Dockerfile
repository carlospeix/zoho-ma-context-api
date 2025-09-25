FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ARG USER_NAME
ARG USER_UID
ARG USER_GID

# You should only one of the following commands.
# If the user is already created in the image, we adjust the ids if necessary
# RUN if [ "$USER_GID" != "1000" ] || [ "$USER_UID" != "1000" ]; then groupmod --gid $USER_GID $USER_NAME && usermod --uid $USER_UID --gid $USER_GID $USER_NAME; fi
# If the user is NOT created in the image, we create it with the proper ids
RUN addgroup --gid $USER_GID $USER_NAME && adduser --disabled-password --gecos '' --uid $USER_UID --gid $USER_GID $USER_NAME

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get -y update && export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y --no-install-recommends install curl git

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt && \
    rm -rf /tmp/pip-tmp
