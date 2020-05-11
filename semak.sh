#/bin/bash

cd /opt/tools/limit

saya=`whoami`
max=`grep $saya limit.dat | cut -d';' -f2`

dahpakai=`cat uselog.$saya`

minitdahpakai=$((dahpakai*10/60))
#echo $max
#echo $dahpakai
#echo $minitdahpakai


baki=$((max-minitdahpakai ))
echo "baki masa utk "$saya": "$baki" minit"

read tamat
