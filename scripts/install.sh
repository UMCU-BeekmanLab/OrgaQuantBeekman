#!/bin/bash
# Unpack environment 
ENV = OrgaQuant
mkdir -p $ENV
tar -xzf $ENV.tar.gz -C $ENV

# Use python without activating or fixing the prefixes. Most python
# libraries will work fine, but things that require prefix cleanups
# will fail.
./$ENV/bin/python

# Activate the environment. This adds `my_env/bin` to your path
source $ENV/bin/activate

# Cleanup prefixes from in the active environment.
# Note that this command can also be run without activating the environment
# as long as some version of python is already installed on the machine.
conda-unpack