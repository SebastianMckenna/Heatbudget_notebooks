#!/bin/bash

DL_PATH='https://dsrs.atmos.umd.edu/DATA/soda3.4.2/REGRIDED/ocean/soda3.4.2_mn_ocean_reg_'
outdir='/home/z5113258/Documents/SODA3.4.2/'

#fucntion to regrid file
regrid_deep () {
        #$1 = varibale name
        #$2 = depth_idx
        #$5 = file
        #mk outdire if not there
        OUTDIR=$outdir/$1_$2
        mkdir -p $OUTDIR
        FILE="${3##*/}"
        cdo -selname,$1 $3 $OUTDIR/tmp.nc
        for i in 0{1..9} {10..25}; do
            echo "doing $i here"
            cdo -remapbil,global_1 -sellevidx,$i $OUTDIR/tmp.nc $OUTDIR/'lev_'$i'.nc'
        done
        #now merge all levels from files generated and delete intermediate files
        cdo -merge $OUTDIR/lev* $OUTDIR/$FILE
        rm $OUTDIR/tmp.nc
        rm $OUTDIR/lev*
}

regrid_shallow () {
        #$1 = varibale name
        #$2 = depth_idx
        #$5 = file
        #mk outdire if not there
        OUTDIR=$outdir/$1_$2
        mkdir -p $OUTDIR
        FILE="${3##*/}"
        cdo -selname,$1 $3 $OUTDIR/tmp.nc
        for i in 0{1..7}; do
            echo "doing $i here"
            cdo -remapbil,global_1 -sellevidx,$i $OUTDIR/tmp.nc $OUTDIR/'lev_'$i'.nc'
        done
        #now merge all levels from files generated and delete intermediate files
        cdo -merge $OUTDIR/lev* $OUTDIR/$FILE
        rm $OUTDIR/tmp.nc
        rm $OUTDIR/lev*
}


regrid_nolevs () {
        #$1 = varibale name
        #$2 = file
        #mk outdire if not there
        OUTDIR=$outdir/$1
        mkdir -p $OUTDIR
        FILE="${2##*/}"
        cdo -selname,$1 $2 $OUTDIR/tmp.nc
        cdo -remapbil,global_1 $OUTDIR/tmp.nc $OUTDIR/$FILE
        rm $OUTDIR/tmp.nc
}

#regrid "temp" "25" "soda3.4.2_mn_ocean_reg_1980.nc"

#put totgether paths into textfiles to then read in wget command
for year in {1980..2020}; do
    echo $DL_PATH$year.nc >> $outdir/file_list.txt 
done

cat $outdir/file_list.txt | while read file
do
        mkdir -p $outdir/full
	wget ${file} -P $outdir/full/
	#process file
	name=`echo ${file} | sed 's:.*/::'`
	echo $name
	regrid_deep "temp" "25" $outdir/full/$name
	regrid_shallow "temp" "7" $outdir/full/$name
	regrid_shallow "u" "7" $outdir/full/$name
	regrid_shallow "v" "7" $outdir/full/$name
	regrid_nolevs "net_heating" $outdir/full/$name
	regrid_nolevs "mlt" $outdir/full/$name
	regrid_nolevs "taux"  $outdir/full/$name
	regrid_nolevs "tauy"  $outdir/full/$name
	#now remove file aftyer getting data from it
	rm $outdir/full/$name
	#exit
done

