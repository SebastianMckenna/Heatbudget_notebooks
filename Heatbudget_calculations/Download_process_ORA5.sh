#!/bin/bash

#getting ORAS5 files

#wget https://icdc.cen.uni-hamburg.de/thredds/fileServer/ftpthredds/EASYInit/oras5/r1x1/vozocrte/opa0/vozocrte_ORAS5_1m_2018_r1x1.tar.gz


bas_url='https://icdc.cen.uni-hamburg.de/thredds/fileServer/ftpthredds/EASYInit/oras5/r1x1/'
var='sometauy'
run='/opa0/'
ext='_r1x1.tar.gz'
#tmask2D_r1x1.nc  tmask_r1x1.nc  umask2D_r1x1.nc  umask_r1x1.nc  vmask2D_r1x1.nc  vmask_r1x1.nc
LSM_file='vmask2D_r1x1.nc'

#generate file list
for year in {1980..2018}; do
    filename=$(echo $var"_ORAS5_1m_"$year$ext)
    echo $bas_url$var$run$filename >> ~/Documents/ORAS5/$var.txt
done
#function to regrid
regrid_shallow () {
        #$1 = depth_idx
        #$2 = file
        #mk outdire if not there
        OUTDIR=$outdir/$3
        mkdir -p $OUTDIR
        FILE="${1##*/}"
	LSM=$outdir/LSM/$2
        for i in 0{1..9} {10..21}; do
            echo "doing $i here"
	    cdo ifthen $LSM $1 $OUTDIR/tmp.nc
            cdo -remapbil,global_1 -sellevidx,$i $OUTDIR/tmp.nc $OUTDIR/'lev_'$i'.nc'
        done
        #now merge all levels from files generated and delete intermediate files
        cdo -merge $OUTDIR/lev* $OUTDIR/$FILE
        rm $OUTDIR/tmp.nc
        rm $OUTDIR/lev*
}

regrid_2d () {
        #$1 = depth_idx
        #$2 = file
        #mk outdire if not there
        OUTDIR=$outdir/$3
        mkdir -p $OUTDIR
        FILE="${1##*/}"
        LSM=$outdir/LSM/$2
        cdo ifthen $LSM $1 $OUTDIR/tmp.nc
        cdo -remapbil,global_1 $OUTDIR/tmp.nc $OUTDIR/$FILE
        rm $OUTDIR/tmp.nc
}



outdir='/home/z5113258/Documents/ORAS5/'
#mkdir -p ${outdir}LSM
##downlaod LSM
#wget -P ${outdir}LSM https://icdc.cen.uni-hamburg.de/thredds/fileServer/ftpthredds/EASYInit/oras5/r1x1/LSM_r1x1/LSM_r1x1.tar.gz
##untar LSM files
#tar -xf $outdir/LSM/LSM_r1x1.tar.gz -C $outdir/LSM

#now go through urls, download and process data through LSM and remap
cat $outdir$var.txt | while read file
do
        mkdir -p $outdir/full
	mkdir -p $outdir/full/$var
        #DL tar.gz file for this list
	wget ${file} -P $outdir/full/
	name=`echo ${file} | sed 's:.*/::'`
        #untar file into directory for var
	tar -xf $outdir/full/$name -C $outdir/full/$var
	#process file
	var1=$(echo $name | cut -d '.' -f1 | cut -d '_' -f 1,2,3,4)
	echo $var1
	for M in 0{1..9} {10..12};do
	    ncfile=`echo "${var1}${M}_r1x1.nc"`
	    #now use cdo on the file
	    #regrid_shallow "$outdir/full/$var/$ncfile" "$LSM_file" "${var}_70"
            regrid_2d "$outdir/full/$var/$ncfile" "$LSM_file" "${var}_surf"
	    #remove file used 
	    rm $outdir/full/$var/$ncfile
	done
        #now remove file aftyer getting data from it
        rm $outdir/full/$name
        #exit
done


