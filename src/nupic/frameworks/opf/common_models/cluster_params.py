# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2015, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import csv
import json
import numpy as np
import os
from pkg_resources import resource_stream


def setRandomEncoderParams(params, minVal, maxVal, minResolution):
  """
  Given model params, figure out the correct parameters for the
  RandomDistributed encoder. Modifies params in place.
  """
  encodersDict = (
    params["modelConfig"]["modelParams"]["sensorParams"]["encoders"]
  )

  for encoder in encodersDict.itervalues():
    if encoder:
      if encoder["type"] == "RandomDistributedScalarEncoder":
        resolution = max(minResolution,
                         (maxVal - minVal) / encoder.pop("numBuckets")
                        )
        encodersDict["c1"]["resolution"] = resolution



def getScalarMetricWithTimeOfDayParams(metricData,
                                       minVal=None,
                                       maxVal=None,
                                       minResolution=None,
                                       useRandomEncoder=True):
  """
    Return an ordered list of JSON strings that can be used to create an
    anomaly model for OPF's ModelFactory.

    :param metricData: numpy array of metric data. Used to calculate minVal
      and maxVal if either is unspecified

    :param minVal: minimum value of metric. Used to set up encoders. If None
      will be derived from metricData.

    :param maxVal: maximum value of metric. Used to set up input encoders. If
      None will be derived from metricData

    :param minResolution: minimum resolution of metric. Used to set up
      encoders.  If None, will use default value of 0.001.

    :param useRandomEncoder: if True, use RandomDistributedScalarEncoder
      instead of ScalarEncoder

    Assumptions:
        The timeStamp field corresponds to c0
        The predicted field corresponds to c1
  """
  # Default values
  if minResolution is None:
    minResolution = 0.001

  # Read a sorted list of parameters from the appropriate directory
  if useRandomEncoder:
    paramsDirectory = "anomaly_params_random_encoder"
  else:
    paramsDirectory = "scalarMetricWithTimeOfDayAnomalyParams"

  with resource_stream(
        "nupic.frameworks.opf.common_models",
        os.path.join(paramsDirectory, "paramOrder.csv")
      ) as fileObj:
    paramFiles = next(csv.reader(fileObj))

  paramSets = []

  # Compute min and/or max from the data if not specified
  if minVal is None or maxVal is None:
    compMinVal, compMaxVal = rangeGen(metricData)
    if minVal is None:
      minVal = compMinVal
    if maxVal is None:
      maxVal = compMaxVal

  # Handle the corner case where the incoming min and max are the same
  if minVal == maxVal:
    maxVal = minVal + 1

  # Iterate over the parameters for each model and replace the appropriate
  # min/max values to the computed ones.
  for filename in paramFiles:
    with resource_stream("nupic.frameworks.opf.common_models",
                         os.path.join(paramsDirectory, filename)) as infile:
      paramSet = json.load(infile)

    encodersDict= (
      paramSet["modelConfig"]["modelParams"]["sensorParams"]["encoders"]
    )

    if useRandomEncoder:
      setRandomEncoderParams(paramSet, minVal, maxVal, minResolution)
    else:
      encodersDict["c1"]["maxval"] = maxVal
      encodersDict["c1"]["minval"] = minVal

    paramSets.append(paramSet)

  return paramSets



def rangeGen(data, std=1):
  """
  Return reasonable min/max values to use given the data.
  """
  dataStd = np.std(data)
  if dataStd == 0:
    dataStd = 1
  minval = np.min(data) -  std * dataStd
  maxval = np.max(data) +  std * dataStd
  return minval, maxval
