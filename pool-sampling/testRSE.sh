#!/bin/bash
coeset=("N_N" "0_1" "1_0" "1_1" "2_0" "2_1")
for((i=1;i<6;i++))
do  
    sed -i "s/${coeset[i-1]}/${coeset[i]}/g" testModel.py
    echo "*********** coe = ${coeset[i]} *************"
    python testModel.py
done
sed -i "s/${coeset[5]}/${coeset[0]}/g" testModel.py
