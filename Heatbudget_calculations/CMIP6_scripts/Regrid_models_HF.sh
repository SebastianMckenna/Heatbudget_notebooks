#!/bin/bash
#PBS -P e14
#PBS -l walltime=04:00:00
#PBS -l mem=28GB
#PBS -q normalbw
#PBS -l wd
#PBS -l storage=gdata/oi10+gdata/fs38+gdata/e14+scratch/e14+gdata/hh5

module use /g/data3/hh5/public/modules
module load netcdf conda/analysis3

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
        #cdo  sellonlatbox,30,-70,-30,30 \
        cdo -remapbil,global_1 $1 $OUTDIR/$FILE
}

loop_var() {
        outdir='/g/data/e14/sm2435/CMIP6/CMIP6/'
	cat /home/561/sm2435/new_CMIP6_scripts/models.txt_OG | while read model
        #get model name
        do
            cat /home/561/sm2435/new_CMIP6_scripts/${model}_list.txt | while read line
            #read the directory list file
            do
                for file in $line; do
                #read each directory
                    vari=$(echo $file | grep -oP '(?<=Amon/).*?(?=/g)')
                    #extract var name from dir
                    for ncfile in ${file}/*.nc; do
                        #go through each file in dir
                        if [[ $vari = $1 ]]; then
                            regrid_2d $ncfile $model $vari
			    #echo "$ncfile"
                        fi
                    done
                done
            done
        done
}

loop_vari_fx() {
        outdir='/g/data/e14/sm2435/CMIP6/CMIP6/'
        cat /home/561/sm2435/new_CMIP6_scripts/models.txt_OG | while read model
        #get model name
        do
            cat /home/561/sm2435/new_CMIP6_scripts/${model}_list.txt | while read line
            #read the directory list file
            do
                for file in $line; do
                #read each directory
                    vari=$(echo $file | grep -oP '(?<=fx/).*?(?=/g)')
                    #extract var name from dir
                    for ncfile in ${file}/*.nc; do
                        #go through each file in dir
                        if [[ $vari = $1 ]]; then
                            regrid_2d $ncfile $model $vari
                            #echo "$ncfile"
                        fi
                    done
                done
            done
        done
}





loop_vari_fx "sftlf"
exit
loop_var "hfss"
loop_var "hfss"
loop_var "rsds"
loop_var "rsus"
loop_var "rlds"
loop_var "rlus"

exit

