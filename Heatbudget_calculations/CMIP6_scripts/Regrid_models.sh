#!/bin/bash
module use /g/data3/hh5/public/modules
module load netcdf conda

####define fucmntion for surface level vars regridding at smaller extent
regrid_shallow () {
        #$1 = depth_idx
        #$2 = file
        #mk outdire if not there
        OUTDIR=$outdir/$2/$3
        mkdir -p $OUTDIR
        FILE="${1##*/}"
        #LSM=$outdir/LSM/$2
        for i in 0{1..9} {10..21}; do
            echo "doing $i here"
            #cdo ifthen $LSM $1 $OUTDIR/tmp.nc
            cdo sellonlatbox,-180,180,-30,30 \
		-remapbil,global_1 -sellevidx,$i $1 $OUTDIR/'lev_'$i'.nc'
        done
        #now merge all levels from files generated and delete intermediate files
        cdo -merge $OUTDIR/lev* $OUTDIR/$FILE
        rm $OUTDIR/lev*
}

regrid_2d () {
        #$1 = file
        #$2 = model
	#$3 = vari
        #mk outdire if not there
        OUTDIR=$outdir/$2/$3
        mkdir -p $OUTDIR
        FILE="${1##*/}"
        cdo  sellonlatbox,30,-70,-30,30 \
             -remapbil,global_1 $1 $OUTDIR/$FILE
}

outdir='/scratch/e14/sm2435/CMIP6/'

cat /home/561/sm2435/CMIP6_scripts/models.txt_OG | while read model
#get model name
do
    cat /home/561/sm2435/CMIP6_scripts/${model}_list.txt | while read line
    #read the directory list file
    do
	for file in $line; do
	#read each directory
	    vari=$(echo $file | grep -oP '(?<=Omon/).*?(?=/gn)')
	    #extract var name from dir
	    for ncfile in ${file}/*1850*.nc; do
		#go through each file in dir
		if [ $vari = "thetao" ]; then
		    echo $vari
		    regrid_shallow $ncfile $model $vari
		elif [ $vari = "hfds" ]
		then
                    echo $vari
		    #regrid data
		    regrid_2d $ncfile $model $vari
		else
		    echo "not"
		fi
	    done
	done
    done
done
exit
