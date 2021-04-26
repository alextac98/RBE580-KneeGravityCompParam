################
#### About #####
################
# This script is run by the user if environment variables are needed that can't get automatically fetched
# Ex. [DISPLAY] environment variable can be different if run in a terminal vs run by VS Code when launching devcontainers

##############################################
##### Get all necessary display settings #####
##############################################
DISPLAY_ENV=.devcontainer/display.env
DISPLAY=$(echo $DISPLAY)

rm $DISPLAY_ENV

printf "DISPLAY=%s\n" "$DISPLAY" >> $DISPLAY_ENV