#!/bin/bash

GODAS='/home/z5113258/Documents/GODAS/'
hflux='thflx'
pottemp='pottmp'
ucur='ucur'
vcur='vcur'
dzdt='dzdt'




OUTDIR='/home/z5113258/Documents/GODAS/outputs/'

mkdir -p $OUTDIR


name='godas'


for file in $GODAS/$pottemp/*.nc; do
   FILE="${file##*/}"
   cdo -sellevel,0/70 $file $OUTDIR/temp.nc
   cdo -remapbil,global_1 $OUTDIR/temp.nc $OUTDIR/$FILE
   rm $OUTDIR/temp.nc
done


for file in $GODAS/$ucur/*.nc; do
    FILE="${file##*/}"
    cdo -sellevel,0/70 $file $OUTDIR/temp.nc
    cdo -remapbil,global_1 $OUTDIR/temp.nc $OUTDIR/$FILE
    rm $OUTDIR/temp.nc
done

for file in $GODAS/$vcur/*.nc; do
    FILE="${file##*/}"
    cdo -sellevel,0/70 $file $OUTDIR/temp.nc
    cdo -remapbil,global_1 $OUTDIR/temp.nc $OUTDIR/$FILE
    rm $OUTDIR/temp.nc
done

for file in $GODAS/$dzdt/*.nc; do
    FILE="${file##*/}"
    cdo -sellevel,0/70 $file $OUTDIR/temp.nc
    cdo -remapbil,global_1 $OUTDIR/temp.nc $OUTDIR/$FILE
    rm $OUTDIR/temp.nc
done
    
for file in $GODAS/$hflux/*.nc; do
    FILE="${file##*/}"
    cdo -b 64 -remapbil,global_1 $file $OUTDIR/$FILE
done




