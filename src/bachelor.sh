#!/usr/bin/env bash
#$ -binding linear:1 #python only needs 1 without threading
#$ -l mem_free=1000M


~/miniconda3/envs/ba/bin/python3.9 ~/OPM/src/main.py