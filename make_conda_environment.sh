#!/bin/bash

COLOR="\033[40m\033[32m"
UNCOLOR="\033[0m"

NAME=py2gift

# only required if "anaconda" is not in the path
source $HOME/anaconda3/etc/profile.d/conda.sh

conda create --yes -n $NAME python=3 jupyterlab numpy pandas ruamel.yaml tqdm pyyaml paramiko colorama -c defaults -c conda-forge

echo -e new environment is \"$COLOR$NAME$UNCOLOR\"

conda activate $NAME

pip install gift-wrapper nbdev

# the environment is exported into a yaml file
conda env export --no-builds --from-history -f environment.yml
