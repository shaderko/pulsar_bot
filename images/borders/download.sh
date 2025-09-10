#!/bin/bash
for i in `seq 21`
do
	URL="https://raw.communitydragon.org/pbe/plugins/rcp-fe-lol-static-assets/global/default/images/uikit/themed-level-ring/theme-${i}-simplified-border.png"
	echo $URL
   	wget $URL
done