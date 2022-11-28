# svd_directions
The data and notebook for the SVD directions LW post. The data consisting of the npy files of correct directions for the autolabelling experiments as well as json files of all prompts and model responses can be found in the data folder. The PySvelte code for the visualizations can be found in the visualizations folder (to get these visualizations working outside of the notebook, you will need to install pysvelte (from [here](https://github.com/TomFrederik/PySvelte) and copy across the files. You can see how to do so in the installation cell in the notebook.

# Setup:
- You will need node, npm and pytorch installed before running the notebook. 
- Other dependencies should be installed by running `./setup.sh` - this installs python dependencies and PySvelte for visualizations.
