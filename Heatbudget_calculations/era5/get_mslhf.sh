#!/bin/bash
#script to get the ERA5 data for wind stress
#first get wind stress, then mask with LSM. Then regrid data, lastly save data
lsm_dir="/g/data/rt52/era5/single-levels/monthly-averaged/lsm/"
lhf_dir="/g/data/rt52/era5/single-levels/monthly-averaged/mslhf/"
out_lhf="/g/data/e14/sm2435/ERA5/lhf/"
ERA5_dir="/g/data/e14/sm2435/ERA5/"
#create land sea mask
cdo -lec,0  /g/data/rt52/era5/single-levels/monthly-averaged/lsm/2000/lsm_era5_moda_sfc_20000101-20000131.nc ${ERA5_dir}mask.nc

for year in {1980..2020}; do
    for FILE in $lhf_dir$year/*.nc; do
	echo $FILE, ${FILE##*/}
	cdo -f nc -div $FILE ${ERA5_dir}mask.nc ${ERA5_dir}temp.nc
	cdo -remapbil,global_1 ${ERA5_dir}temp.nc $out_lhf${FILE##*/}
    done
done
