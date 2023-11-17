#!/bin/bash

#this bash script will download GODAS files locally to then perform analysis

#define paths to downlaod from and to
DL_PATH='https://downloads.psl.noaa.gov/Datasets/godas/'
outdir='/home/z5113258/Documents/GODAS/'
hflux='thflx'
pottemp='pottmp'
ucur='ucur'
vcur='vcur'
dtdz='dzdt'
dbss_obml='dbss_obml'

#dzdt.1980.nc

#put totgether paths into textfiles to then read in wget command
for year in {1980..2020}; do 
    ##echo $DL_PATH$hflux.$year.nc >> ~/Documents/GODAS/hflux_url.txt    
    #echo $DL_PATH$pottemp.$year.nc >> ~/Documents/GODAS/pottemp_url.txt
    #echo $DL_PATH$ucur.$year.nc >> ~/Documents/GODAS/ucur_url.txt
    ##echo $DL_PATH$vcur.$year.nc >> ~/Documents/GODAS/vcur_url.txt
    #echo $DL_PATH$dtdz.$year.nc >> ~/Documents/GODAS/dtdz_url.txt
    echo $DL_PATH$dbss_obml.$year.nc >> ~/Documents/GODAS/dbss_obml_url.txt
done

#wget -i ~/Documents/GODAS/hflux_url.txt -P $outdir$hflux
#wget -i ~/Documents/GODAS/pottemp_url.txt -P $outdir$pottemp
#wget -i ~/Documents/GODAS/ucur_url.txt -P $outdir$ucur
#get -i ~/Documents/GODAS/vcur_url.txt -P $outdir$vcur
#wget -i ~/Documents/GODAS/dtdz_url.txt -P $outdir$dtdz
wget -i ~/Documents/GODAS/dbss_obml_url.txt -P $outdir$dbss_obml
