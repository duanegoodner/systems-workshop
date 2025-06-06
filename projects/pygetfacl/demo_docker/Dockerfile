FROM python:3.10.0

SHELL [ "/bin/bash", "--login", "-c" ]
ENV USER_A=user_a

# create user w/ sudo rights; do everything else as that user
RUN useradd -s /bin/bash -m ${USER_A} \
    && apt-get update \
    && apt-get install -y sudo acl \
    && echo ${USER_A} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USER_A} \
    && chmod 0440 /etc/sudoers.d/${USER_A}
USER ${USER_A}

RUN pip install git+https://github.com/duanegoodner/pygetfacl

# set up container entrypoint
COPY entrypoint.sh ./
RUN sudo chown ${USER_A}:${USER_A} ./entrypoint.sh && sudo chmod u+x ./entrypoint.sh
ENTRYPOINT [ "/bin/bash", "./entrypoint.sh"]

