################
#### About #####
################
# This script runs on the host machine before the container is created. 
# Commands execute from the [workspaceFolder]
# See for more info: https://code.visualstudio.com/docs/remote/devcontainerjson-reference

#############################
# Set up User and Group IDs #
#############################
USER_ID=$(id -u)
GROUP_ID=$(id -g)
BUILD_ENV=.devcontainer/build.env

rm $BUILD_ENV

printf "USER_ID=%s\n" "$USER_ID" >> $BUILD_ENV
printf "GROUP_ID=%s\n" "$GROUP_ID" >> $BUILD_ENV

##########################################
# Set up x-server x-authentication files #
##########################################
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth

printf "XSOCK=%s\n" "$XSOCK" >> $BUILD_ENV
printf "XAUTH=%s\n" "$XAUTH" >> $BUILD_ENV
printf "XDG_RUNTIME=%s\n" "$XDG_RUNTIME_DIR" >> $BUILD_ENV

rm $XAUTH && touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -

DISPLAY=$(echo $DISPLAY)
printf "DISPLAY=%s\n" "$DISPLAY" >> $BUILD_ENV