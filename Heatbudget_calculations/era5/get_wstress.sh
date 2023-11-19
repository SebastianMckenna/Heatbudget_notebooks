#!/bin/bash
#script to get the ERA5 data for wind stress
#first get wind stress, then mask with LSM. Then regrid data, lastly save data
lsm_dir="/g/data/rt52/era5/single-levels/monthly-averaged/lsm/"
ewss_dir="/g/data/rt52/era5/single-levels/monthly-averaged/iews/"
nsss_dir="/g/data/rt52/era5/single-levels/monthly-averaged/inss/"
out_u="/g/data/e14/sm2435/ERA5/uss/"
out_v="/g/data/e14/sm2435/ERA5/vss/"
ERA5_dir="/g/data/e14/sm2435/ERA5/"
#create land sea mask
cdo -lec,0  /g/data/rt52/era5/single-levels/monthly-averaged/lsm/2000/lsm_era5_moda_sfc_20000101-20000131.nc ${ERA5_dir}mask.nc

for year in {1980..2020}; do
    for FILE in $ewss_dir$year/*.nc; do
	echo $FILE, ${FILE##*/}
	cdo -f nc -div $FILE ${ERA5_dir}mask.nc ${ERA5_dir}temp.nc
	cdo -remapbil,global_1 ${ERA5_dir}temp.nc $out_u${FILE##*/}
    done
done

for year in {1980..2020}; do
    for FILE in $nsss_dir$year/*.nc; do
        echo $FILE, ${FILE##*/}
        cdo -f nc -div $FILE ${ERA5_dir}mask.nc ${ERA5_dir}temp.nc
        cdo -remapbil,global_1 ${ERA5_dir}temp.nc $out_v${FILE##*/}
    done
done

