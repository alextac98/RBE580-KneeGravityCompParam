##############################################
##### Get all necessary display settings #####
##############################################
DISPLAY_ENV=.devcontainer/display.env
DISPLAY=$(echo $DISPLAY)

rm $DISPLAY_ENV

printf "DISPLAY=%s\n" "$DISPLAY" >> $DISPLAY_ENV