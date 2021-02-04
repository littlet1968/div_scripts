#!/bin/bash
echo $#

read

export MA=$(xdotool search --name $1)
xdotool type --window $MA $2


