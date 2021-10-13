#!/bin/bash
STENCIL=("addsgd4" "addsgd6" "rhs4center" "cheby" "hhz" "hypterm" "j3d7pt" "j3d27pt")

PROCESS=(2 4 8 16)

#for((i=0;i<1;i++))
for((i=0;i<8;i++))
do
    mpirun -np ${PROCESS[0]} ./perf-ga | tee result/log_${STENCIL[i]}.txt
done
