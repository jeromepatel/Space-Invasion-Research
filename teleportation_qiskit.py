# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 21:17:17 2020

@author: jyotm
"""

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import BasicAer
from qiskit import execute

import qiskit
from qiskit import IBMQ
import numpy as np
import operator
import time
import ast
from configparser import RawConfigParser
###############################################################
# Set the backend name and coupling map.
###############################################################
coupling_map = [[0, 1], [0, 2], [1, 2], [3, 2], [3, 4], [4, 2]]
backend = BasicAer.get_backend("qasm_simulator")


#  # Setup the API key for the real quantum computer.
# parser = RawConfigParser()
# parser.read('config.ini')

# # Read configuration values.
# proxies = ast.literal_eval(parser.get('IBM', 'proxies')) if parser.has_option('IBM', 'proxies') else None
# verify = (True if parser.get('IBM', 'verify') == 'True' else False) if parser.has_option('IBM', 'verify') else True
# token = parser.get('IBM', 'key')

# # IBMQ.enable_account(token = token, proxies = proxies, verify = verify)
# run_isInit = True
# provider = IBMQ.get_provider()
# backends = provider.backends()
# backend = qiskit.providers.ibmq.least_busy(backends)

###############################################################
# Make a quantum program for quantum teleportation.
###############################################################
q = QuantumRegister(3, "q")
c0 = ClassicalRegister(1, "cls_0")
c1 = ClassicalRegister(1, "cls_1")
c2 = ClassicalRegister(1, "cls_3")
qc = QuantumCircuit(q, c0, c1, c2, name="teleport")

# Prepare an initial state
#qc.u3(0.3, 0.2, 0.1, q[0])

# Prepare a Bell pair
qc.h(q[1])
qc.cx(q[1], q[2])

# Barrier following state preparation
qc.barrier()

# Measure in the Bell basis
qc.cx(q[0], q[1])
qc.h(q[0])
qc.measure(q[0], c0[0])
qc.measure(q[1], c1[0])

# Apply a correction
qc.barrier()
qc.z(q[2]).c_if(c0, 1)
qc.x(q[2]).c_if(c1, 1)
qc.measure(q[2], c2[0])

print(qc.draw('mpl'))
###############################################################
# Execute.
# Experiment does not support feedback, so we use the simulator
###############################################################

# First version: not mapped
initial_layout = {q[0]: 0,
                  q[1]: 1,
                  q[2]: 2}
job = execute(qc, backend=backend, coupling_map=None, shots=1024,
             initial_layout=initial_layout )

result = job.result()
print(result.get_counts(qc))

# Second version: mapped to 2x8 array coupling graph
job = execute(qc, backend=backend, coupling_map=coupling_map, shots=1024,
              initial_layout=initial_layout)
result = job.result()
print(result.get_counts(qc))
# Both versions should give the same distribution