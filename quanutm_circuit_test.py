# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 11:40:12 2020

@author: jyotm
"""


from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import BasicAer
from qiskit import execute

###############################################################
# Set the backend name and coupling map.
###############################################################
coupling_map = [[0, 1], [0, 2], [1, 2], [3, 2], [3, 4], [4, 2]]
backend = BasicAer.get_backend("qasm_simulator")

###############################################################
# Make a quantum program for quantum teleportation.
###############################################################
# q = QuantumRegister(1, "q")
# c0 = ClassicalRegister(1, "c0")
# c1 = ClassicalRegister(1,'c1')

# qc = QuantumCircuit(q, c0,c1, name="teleport")


# qc.h(q[0])



# qc.measure(q[0], c0[0])

# qc.x(q)

# qc.measure(q[0],c1[0])
n = 1
q = QuantumRegister(n, "qbit") # n qubits
#a = QuantumRegister(1) # one ancilla qubit
c = ClassicalRegister(n, 'cls') # n classical bits for output

qc = QuantumCircuit(q,c)

qc.u3(0.3, 0.2, 0.1, q[0])

#qc.x(a[0]) 
#qc.measure(a[0],c[0]) # measure the ancilla to one of the classical bits

qc.measure(q,c) # measure the n qubits to the n bits (overwriting the output from the previous measurement

print(qc.draw('mpl'))
###############################################################
# Execute.
# Experiment does not support feedback, so we use the simulator
###############################################################

# First version: not mapped
job = execute(qc, backend=backend, coupling_map=None, shots=1024)
result = job.result()
print(result.get_counts(qc))


# Both versions should give the same distribution