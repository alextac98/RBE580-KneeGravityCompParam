FROM python:3

# Set up new user
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Python specific new user setup
RUN printf "export PATH=/home/%s/.local/bin:\$PATH\n" "$USERNAME" >> /home/$USERNAME/.bashrc

# Create Workspace
ARG WORKSPACE=/home/$USERNAME/ws
WORKDIR ${WORKSPACE}

# Remove apt stuff
RUN rm -rf /var/lib/apt/lists/*