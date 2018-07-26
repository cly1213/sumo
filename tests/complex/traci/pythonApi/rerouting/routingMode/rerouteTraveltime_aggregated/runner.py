#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Jakob Erdmann
# @date    2017-01-23
# @version $Id$


from __future__ import print_function
from __future__ import absolute_import
import os
import subprocess
import sys
sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci  # noqa
import sumolib  # noqa

sumoBinary = os.environ["SUMO_BINARY"]
PORT = sumolib.miscutils.getFreeSocketPort()
sumoProcess = subprocess.Popen([sumoBinary,
                                '-c', 'sumo.sumocfg',
                                #'-S', '-Q',
                                '--device.rerouting.adaptation-steps', '120',
                                '--remote-port', str(PORT)], stdout=sys.stdout)

traci.init(PORT)
traci.simulationStep()
while traci.simulation.getMinExpectedNumber() > 0:
    timeS = traci.simulation.getCurrentTime() / 1000
    for vehID in traci.simulation.getDepartedIDList():
        traci.vehicle.setRoutingMode(vehID, traci.constants.ROUTING_MODE_AGGREGATED)
        traci.vehicle.rerouteTraveltime(vehID)
        print("step=%s rerouted=%s" % (timeS, vehID)) 
    #print("step=%s", timeS)
    #for edgeID in traci.edge.getIDList():
    #    print("   edge=%s tt=%s" % (edgeID,
    #        traci.edge.getAdaptedTraveltime(edgeID, timeS)))
    traci.simulationStep()
traci.close()
sumoProcess.wait()
