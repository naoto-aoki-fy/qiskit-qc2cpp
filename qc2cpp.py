import qiskit
from qiskit.circuit.library import HGate, XGate

q = qiskit.QuantumRegister(14)
c = qiskit.ClassicalRegister(14)
qc = qiskit.QuantumCircuit(q, c)

qc.x(q[0])
qc.cx(q[0], q[3])
qc.ccx(q[0], q[1], q[2])
qc.mcx(q[1:6], q[0])

qc.append(XGate().control(2, ctrl_state=0b10), [q[0], q[1], q[4]])

qc.h(q[0])
qc.ch(q[0],q[1])
qc.append(HGate().control(13), q)

qc.measure(q[2], c[1])
qc.measure(q[3], c[0])

for gate in qc.data:
    for qubit in gate.qubits:
        register_size = qubit._register.size
        register_name = qubit._register.name
        qubit_index = qubit._index
    for clbit in gate.clbits:
        register_size = clbit._register.size
        register_name = clbit._register.name
        clbit_index = clbit._index

quantum_registers_set = set()
classical_registers_set = set()

for gate in qc.data:
    for qubit in gate.qubits:
        quantum_registers_set.add(qubit._register)
    for clbit in gate.clbits:
        classical_registers_set.add(clbit._register)

quantum_registers_list = tuple(quantum_registers_set)
classical_registers_list = tuple(classical_registers_set)

def pack_registers(registers_list: list):
    xbit2num_dict = {}
    num2xbit_list = []

    xbit_num = 0
    for register in registers_list:
        for xbit in register:
            xbit2num_dict[xbit] = xbit_num
            assert len(num2xbit_list) == xbit_num
            num2xbit_list.append(xbit)
            xbit_num += 1

    return xbit2num_dict, num2xbit_list

qubit2num_dict, num2qubit_list = pack_registers(quantum_registers_list)
clbit2num_dict, num2clbit_list = pack_registers(classical_registers_list)

num_qubits = len(num2qubit_list)
print(f"set_num_qubits({num_qubits});")
num_clbits = len(num2clbit_list)
print(f"set_num_clbits({num_clbits});")

def get_base_gate_name(s: str) -> str:
    import re
    return re.sub(r'^(?:mc|cc|c\d*)|_o\d+$', '', s)

for gate in qc.data:
    qubit_num_list = tuple(qubit2num_dict[qubit] for qubit in gate.qubits)
    clbit_num_list = tuple(clbit2num_dict[clbit] for clbit in gate.clbits)
    if gate.operation.name == "measure":
        print(f"sim.measure({{{','.join(str(qubit_num) for qubit_num in qubit_num_list)}}}, {{{','.join(str(clbit_num) for clbit_num in clbit_num_list)}}});")
    else:
        no_ctrl_gate_name = get_base_gate_name(gate.operation.name)
        ctrl_qubit_num_list = qubit_num_list[:-1]
        target_qubit_num = qubit_num_list[-1]

        ctrl_state = getattr(gate.operation, 'ctrl_state', None)
        neg_ctrl_qubit_num_list = []
        if ctrl_state is not None:
            for i, ctrl_qubit_num in enumerate(ctrl_qubit_num_list):
                if not (ctrl_state >> i) & 1:
                    neg_ctrl_qubit_num_list.append(ctrl_qubit_num)

        print(
            f"sim.gate_{no_ctrl_gate_name}({{{target_qubit_num}}}, {{{','.join(str(ctrl_qubit_num) for ctrl_qubit_num in ctrl_qubit_num_list)}}}, {{{','.join(str(num) for num in neg_ctrl_qubit_num_list)}}});"
        )
