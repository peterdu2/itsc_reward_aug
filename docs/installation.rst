Installation Guide
******************

Open the command prompt and change to the directory you wish to download the package into. Run the following command to clone the repository, as well as the submodules, and change to the top-level directory:
::
	git clone --recursive https://github.com/sisl/AdaptiveStressTestingToolbox
	cd <Path-To-AdaptiveStressTestingToolbox>/AdaptiveStressTestingToolbox

If you have already cloned the repo, you can run the following command to download the submodules:
::
	cd <Path-To-AdaptiveStressTestingToolbox>/AdaptiveStressTestingToolbox
	git submodule update --init --recursive

If you have done the previous steps correctly, there should be a ``AdaptiveStressTestingToolbox/garage`` folder. Please see the `garage installation page <https://rlgarage.readthedocs.io/en/latest/user/installation.html>`_ for details on how to get all of their dependencies. Once garage is installed, create the Conda environment by running the following command from the top-level garage directory:
::
	cd <Path-To-AdaptiveStressTestingToolbox>/AdaptiveStressTestingToolbox/garage
	conda env create -f environment.yml

Once the environment has been created, activate it by running:
::
	source activate garage

More information on Conda environments can be found in their `documentation <https://conda.io/en/latest/>`_. Finally, add everthing to your ``PYTHONPATH`` like shown below:
::
	export PYTHONPATH=$PYTHONPATH:$PWD/Toolbox/garage:$PWD/TestCases:$PWD/Toolbox:$PWD/Toolbox/pydot

To validate your installation, please run the following:
::
	python <Path-To-AdaptiveStressTestingToolbox>/AdaptiveStressTestingToolbox/TestCases/validate_install.py

You should see the method run for a single iteration, then print out a success message. You are now able to run this package. For more information on how to interface this package with your work, please see the tutorial.
