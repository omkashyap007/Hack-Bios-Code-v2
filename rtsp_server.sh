#!/bin/bash
array[0]="none"
array[1]="negative"
array[2]="solarise"
array[3]="sketch"
array[4]="denoise"
array[5]="emboss"
array[6]="oilpant"
array[7]="hatch"
array[8]="gpen"
array[9]="pastel"
array[10]="watercolour"
array[11]="film"
array[12]="blur"
array[13]="saturation"
array[14]="colourswap"
array[15]="washedout"
array[16]="posterise"
array[17]="colourpoint"
array[18]="colourbalance"
array[19]="cartoon"
size=${#array[@]}
index=$(($RANDOM % $size))
echo ${array[$index]}
sleep 1
raspivid -t 0 -w 800 -h 600 -ifx ${array[$index]} -fps 15 -l -o tcp://0.0.0.0:5000