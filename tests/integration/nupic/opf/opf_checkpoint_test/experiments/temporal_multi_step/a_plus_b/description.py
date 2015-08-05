
# ----------------------------------------------------------------------
#  Copyright (C) 2011 Numenta Inc. All rights reserved.
#
#  The information and source code contained herein is the
#  exclusive property of Numenta Inc. No part of this software
#  may be used, reproduced, stored or distributed in any form,
#  without explicit written authorization from Numenta Inc.
# ----------------------------------------------------------------------

## This file defines parameters for a prediction experiment.

###############################################################################
#                                IMPORTANT!!!
# This params file is dynamically generated by the RunExperimentPermutations
# script. Any changes made manually will be over-written the next time
# RunExperimentPermutations is run!!!
###############################################################################


from nupic.frameworks.opf.expdescriptionhelpers import importBaseDescription

# the sub-experiment configuration
config ={
  'modelParams' : {'sensorParams': {'encoders': {'c0_timeOfDay': None, 'c0_dayOfWeek': None, 'c1': {'name': 'c1', 'clipInput': True, 'n': 275, 'fieldname': 'c1', 'w': 21, 'type': 'AdaptiveScalarEncoder'}, 'c0_weekend': None}}, 'spParams': {'synPermInactiveDec': 0.052500000000000005}, 'tpParams': {'minThreshold': 11, 'activationThreshold': 14, 'pamLength': 3}, 'clParams': {'alpha': 0.050050000000000004}},
  
  'firstRecord': 0,
  'lastRecord': 500,
}

mod = importBaseDescription('../base.py', config)
locals().update(mod.__dict__)
