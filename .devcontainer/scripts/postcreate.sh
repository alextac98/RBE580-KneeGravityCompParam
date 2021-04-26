################
#### About #####
################
# This script runs inside container after it is created for the first time
# Commands execute from the [workspaceFolder]
# See for more info: https://code.visualstudio.com/docs/remote/devcontainerjson-reference

#################################################
# Make User using local computer user/group IDs #
#################################################
sudo usermod -u $USER_ID user
sudo groupmod -g $GROUP_ID user

###############################
# Install python dependencies #
###############################
pip install -e Vicon/. --no-warn-script-location
pip uninstall GaitCore -y
pip install -e GaitCore/. --no-warn-script-location