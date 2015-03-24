#!/bin/bash

qsub -j eo -S /bin/bash -o . -l nodes=1:ppn=1,pmem=20g,walltime="63:59:00" -d . run_find_corr.sh
