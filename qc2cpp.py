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

# 測定
qc.measure(q[2], c[1])
qc.measure(q[3], c[0])

# qc.draw(output='mpl')

# @title acquire information of the circuit

for gate in qc.data:
    # print(f"gate:")
    # print("  operation:", gate.operation)
    # print("  qubits:")
    for qubit in gate.qubits:
        register_size = qubit._register.size
        register_name = qubit._register.name
        qubit_index = qubit._index
        # print("    ", qubit, register_name, register_size, qubit_index)
    # print("  clbits:")
    for clbit in gate.clbits:
        register_size = clbit._register.size
        register_name = clbit._register.name
        clbit_index = clbit._index
        # print("    ", clbit, register_name, register_size, clbit_index)

# @title gather registers

quantum_registers_set = set()
classical_registers_set = set()

for gate in qc.data:
    for qubit in gate.qubits:
        quantum_registers_set.add(qubit._register)
    for clbit in gate.clbits:
        classical_registers_set.add(clbit._register)

quantum_registers_list = tuple(quantum_registers_set)
classical_registers_list = tuple(classical_registers_set)

# print(quantum_registers_list)
# print(classical_registers_list)

# @title calculate offset of Xbits in order to translate (pack) Xbits to number, and reverse-wise. 

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
# print(qubit2num_dict)
# print(num2qubit_list)

clbit2num_dict, num2clbit_list = pack_registers(classical_registers_list)
# print(clbit2num_dict)
# print(num2clbit_list)

# @title dump circuit information in packed form

num_qubits = len(num2qubit_list)
print(f"set_num_qubits({num_qubits});")
num_clbits = len(num2clbit_list)
print(f"set_num_clbits({num_clbits});")

# def get_base_gate_name(gate_name):
#     print(f"{gate_name=}")
#     if gate_name.startswith("mc"):
#         return gate_name[2:]
#     elif gate_name.startswith("cc"):
#         return gate_name[2:]
#     elif gate_name.startswith("c"):
#         return gate_name[1:]
#     else:
#         return gate_name

# def get_base_gate_name(s: str) -> str:
#     import re
#     print(f"{s=}")
#     # mcから始まる場合
#     if s.startswith("mc"):
#         return s[2:]
#     # ccから始まる場合
#     elif s.startswith("cc"):
#         return s[2:]
#     # c + 数字から始まる場合
#     elif re.match(r"^c\d+", s):
#         return re.sub(r"^c\d+", "", s)
#     elif s.startswith("c"):
#         return s[1:]
#     else:
#         # 該当しない場合はそのまま返す
#         return s

def get_base_gate_name(s: str) -> str:
    import re
    # mc, cc, または c+数字 を先頭から削除
    return re.sub(r'^(?:mc|cc|c\d*)', '', s)


for gate in qc.data:
    # print(f"{dir(gate)=}")
    # print(f"{gate.params=}")
    qubit_num_list = tuple(qubit2num_dict[qubit] for qubit in gate.qubits)
    clbit_num_list = tuple(clbit2num_dict[clbit] for clbit in gate.clbits)
    if gate.operation.name == "measure":
        print(f"sim.measure({{{','.join(str(qubit_num) for qubit_num in qubit_num_list)}}}, {{{','.join(str(clbit_num) for clbit_num in clbit_num_list)}}});")
    else:
        no_ctrl_gate_name = get_base_gate_name(gate.operation.name)
        ctrl_qubit_num_list = qubit_num_list[:-1]
        target_qubit_num = qubit_num_list[-1]
        print(f"sim.gate_{no_ctrl_gate_name}({{{target_qubit_num}}}, {{{','.join(str(ctrl_qubit_num) for ctrl_qubit_num in ctrl_qubit_num_list)}}}, {{}});")
