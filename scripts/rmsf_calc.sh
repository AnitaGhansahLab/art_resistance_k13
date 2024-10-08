#!/bin/bash
#PBS -P CBBI1425
#PBS -N rmsf calculations
#PBS -l select=10:ncpus=24:mpiprocs=24
#PBS -l walltime=48:00:00
#PBS -q normal
#PBS -m abe
#PBS -M ndolling5@gmail.com
#PBS -o ./md.stdout.txt
#PBS -e ./md.stderr.txt

module purge
module load chpc/gromacs/v2016.1dev-noomp-openmpi-2.0.0-gcc-6.2.0

ulimit -s unlimited
OMP_NUM_THREADS=1
NP=`cat ${PBS_NODEFILE} | wc -l`
MPIARGS="--mca btl_openib_allow_ib 1"
pushd $PBS_O_WORKDIR
EXE="gmx_mpi mdrun"


echo "4 4" | gmx_mpi rms -s md.tpr -f md_noPBC.xtc -o rmsf.xvg -tu ns
   
 



