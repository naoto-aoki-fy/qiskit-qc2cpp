# qiskit's QuantumCircuit to C++ converter

qiskit's QuantumCircuit

```python
import qiskit
from qiskit.circuit.library import HGate

q = qiskit.QuantumRegister(14)
c = qiskit.ClassicalRegister(14)
qc = qiskit.QuantumCircuit(q, c)

qc.x(q[0])
qc.cx(q[0], q[3])
qc.ccx(q[0], q[1], q[2])
qc.mcx(q[1:6], q[0])

qc.h(q[0])
qc.ch(q[0],q[1])
qc.append(HGate().control(13), q)

qc.measure(q[2], c[1])
qc.measure(q[3], c[0])
```

`python qc2cpp.py`

C++ code

```c++
set_num_qubits(14);
set_num_clbits(14);
sim.gate_x({0}, {}, {});
sim.gate_x({3}, {0}, {});
sim.gate_x({2}, {0,1}, {});
sim.gate_x({0}, {1,2,3,4,5}, {});
sim.gate_h({0}, {}, {});
sim.gate_h({1}, {0}, {});
sim.gate_h({13}, {0,1,2,3,4,5,6,7,8,9,10,11,12}, {});
sim.measure({2}, {1});
sim.measure({3}, {0});
```