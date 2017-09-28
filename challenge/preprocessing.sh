#!/bin/bash
clear

cat $1 | tr "\n" " " | tr [:upper:] [:lower:] | grep -oP '<text.*?>\K.*?(?=</text>)' > $2