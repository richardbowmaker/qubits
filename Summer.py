
from qiskit import *
from qiskit.providers.aer import QasmSimulator

# implements the addition of two 3 bit numbers as described in dancing with qubits
# section 9.4 (p317), see summer_p317()
#
# It a includes a simpler adder based on 3 full adders
# see summer_full_adders()

def summer():

    print("------ Addition -----")
    for x in range(32):
        for y in range(32):
            s = add_n(5, x, y)
            if s == x + y:
                print("result ", x, " + ", y, " = ", s)
            else:
                print("result ", x, " + ", y, " = ", s, " ****** error *******")


#    addition()
#    subtraction()

def addition():
# calculate all permutations of (0..7) + (0..7) and display the result
    print("------ Addition -----")
    for x in range(8):
        for y in range(8):
            s = add(x, y)
            if s == x + y:
                print("result ", x, " + ", y, " = ", s)
            else:
                print("result ", x, " + ", y, " = ", s, " ****** error *******")

def subtraction():

    print("------ Subtraction -----")
    for x in range(8):
        for y in range(8):
            if x >= y:
                s = subtract(x, y)
                if s == x - y:
                    print("result ", x, " - ", y, " = ", s)
                else:
                    print("result ", x, " - ", y, " = ", s, " ****** error *******")

# add two 3 bit numbers
def add(x, y):

    qr = QuantumRegister(10)
    cr = ClassicalRegister(10)

    circuit = QuantumCircuit(qr, cr)

    # set x value
    set_value(circuit, qr, x, [1, 4, 7])

    # set y value
    set_value(circuit, qr, y, [2, 5, 8])
    circuit.barrier()

    set_carry(circuit, qr, 0, 1, 2, 3)
    circuit.barrier()

    set_carry(circuit, qr, 3, 4, 5, 6)
    circuit.barrier()

    set_carry(circuit, qr, 6, 7, 8, 9)
    circuit.barrier()

    circuit.cx(qr[7], qr[8])
    circuit.barrier()

    set_sum(circuit, qr, 6, 7, 8)
    circuit.barrier()

    set_carry_inverse(circuit, qr, 3, 4, 5 ,6)
    circuit.barrier()

    set_sum(circuit, qr, 3, 4, 5)
    circuit.barrier()

    set_carry_inverse(circuit, qr, 0, 1, 2, 3)
    circuit.barrier()

    set_sum(circuit, qr, 0, 1, 2)
    circuit.barrier()

    circuit.measure(qr, cr)

    simulator = Aer.get_backend('qasm_simulator')
    result = execute(circuit, simulator, shots=1).result()
    counts = result.get_counts(circuit)

    return get_value(counts, [2, 5, 8, 9])

# subtract 3 bit number from a 4 bit number
def subtract(x, y):

    qr = QuantumRegister(10)
    cr = ClassicalRegister(10)

    circuit = QuantumCircuit(qr, cr)

    # set x value
    set_value(circuit, qr, x, [2, 5, 8, 9])

    # set y value
    set_value(circuit, qr, y, [1, 4, 7])

    circuit.barrier()

    set_sum_inverse(circuit, qr, 0, 1, 2)
    circuit.barrier()

    set_carry(circuit, qr, 0, 1, 2, 3)
    circuit.barrier()

    set_sum_inverse(circuit, qr, 3, 4, 5)
    circuit.barrier()

    set_carry(circuit, qr, 3, 4, 5, 6)
    circuit.barrier()

    set_sum_inverse(circuit, qr, 6, 7, 8)
    circuit.barrier()

    circuit.cx(qr[7], qr[8])
    circuit.barrier()

    set_carry_inverse(circuit, qr, 6, 7, 8, 9)
    circuit.barrier()

    set_carry_inverse(circuit, qr, 3, 4, 5, 6)
    circuit.barrier()

    set_carry_inverse(circuit, qr, 0, 1, 2, 3)
    circuit.barrier()

    circuit.measure(qr, cr)

    simulator = Aer.get_backend('qasm_simulator')
    result = execute(circuit, simulator, shots=1).result()
    counts = result.get_counts(circuit)

    return get_value(counts, [2, 5, 8])

def add_full_adders(x, y):

    qr = QuantumRegister(10)
    cr = ClassicalRegister(10)

    circuit = QuantumCircuit(qr, cr)

    # set x value
    set_value(circuit, qr, x, [1, 4, 7])

    # set y value
    set_value(circuit, qr, y, [2, 5, 8])
    circuit.barrier()

    set_full_adder(circuit, qr, 0, 1, 2, 3)
    circuit.barrier()

    set_full_adder(circuit, qr, 3, 4, 5, 6)
    circuit.barrier()

    set_full_adder(circuit, qr, 6, 7, 8, 9)
    circuit.barrier()

    circuit.measure(qr, cr)

    simulator = Aer.get_backend('qasm_simulator')
    result = execute(circuit, simulator, shots=1).result()
    counts = result.get_counts(circuit)

    return get_value(counts, [2, 5, 8, 9])

    return 0

def subtract_full_adders(x, y):
# doesn't work

    qr = QuantumRegister(10)
    cr = ClassicalRegister(10)

    circuit = QuantumCircuit(qr, cr)

    # set x value
    set_value(circuit, qr, x, [1, 4, 7])

    # set y value
    set_value(circuit, qr, y, [2, 5, 8])
    circuit.barrier()

    set_full_adder_inverse(circuit, qr, 6, 7, 8, 9)
    circuit.barrier()

    set_full_adder_inverse(circuit, qr, 3, 4, 5, 6)
    circuit.barrier()

    set_full_adder_inverse(circuit, qr, 0, 1, 2, 3)
    circuit.barrier()

    circuit.measure(qr, cr)

    simulator = Aer.get_backend('qasm_simulator')
    result = execute(circuit, simulator, shots=1).result()
    counts = result.get_counts(circuit)

    return get_value(counts, [2, 5, 8, 9])

# sets a binary value over the specified qubits
def set_value(circuit, qubits, value, bits):
    # bits = list of qubits in order lsb to msb
    v = value
    for bit in bits:
        if v % 2 > 0:
            circuit.x(qubits[bit])
        v = v // 2

# gets a binary value from the specified classical bits
def get_value(counts, bits):
    # bits = list of classical bits in order lsb to msb

    # ---the important code start:----------------------------------------
    lAnswer = [(k[::-1], v) for k, v in counts.items()]
    lAnswer.sort(key=lambda x: x[1], reverse=True)
    Y = []
    for k, v in lAnswer: Y.append([int(c) for c in k])
    # ---the important code end--------------------------------------------
    vs = Y[0]
    v = 0
    for bit in reversed(bits):
        v *= 2
        if (vs[bit] != 0):
            v +=1
    return v

def set_carry(circuit, qubits, bCin, bA, bB, b0):
# qubits to use for full adder
#   bA - arg1
#   bB - arg2
#   bCin - carry in, sum out
#   b0 - |0> in, |Cout> out

    circuit.ccx(qubits[bA], qubits[bB], qubits[b0])
    circuit.cx(qubits[bA], qubits[bB])
    circuit.ccx(qubits[bB], qubits[bCin], qubits[b0])

def set_carry_inverse(circuit, qubits, bCin, bA, bS, bCout):
# qubits to use for full adder
#   bA - arg1
#   bB - arg2
#   bS - carry out, sum in
#   bCout - |0> in, |Cout> in

    circuit.ccx(qubits[bCin], qubits[bS], qubits[bCout])
    circuit.cx(qubits[bA], qubits[bS])
    circuit.ccx(qubits[bA], qubits[bS], qubits[bCout])

def set_full_adder(circuit, qubits, bCin, bA, bB, b0):
# based on p316 of dancing with qubits, added a extra CNOT(Cin, S)
# qubits to use for full adder
#   bA - arg1
#   bB - arg2
#   bCin - carry in, sum out
#   b0 - |0> in, |Cout> out

    circuit.ccx(qubits[bA], qubits[bB], qubits[b0])
    circuit.cx(qubits[bA], qubits[bB])
    circuit.ccx(qubits[bB], qubits[bCin], qubits[b0])
    circuit.cx(qubits[bCin], qubits[bB])

def set_full_adder_inverse(circuit, qubits, bCin, bA, bB, b0):
# based on p316 of dancing with qubits, added a extra CNOT(Cin, S)
# qubits to use for full adder
#   bA - arg1
#   bB - arg2
#   bCin - carry in, sum out
#   b0 - |0> in, |Cout> out

    circuit.cx(qubits[bCin], qubits[bB])
    circuit.ccx(qubits[bB], qubits[bCin], qubits[b0])
    circuit.cx(qubits[bA], qubits[bB])
    circuit.ccx(qubits[bA], qubits[bB], qubits[b0])

def set_sum(circuit, qubits, b1, b2, b3):

    circuit.cx(qubits[b1], qubits[b3])
    circuit.cx(qubits[b2], qubits[b3])

def set_sum_inverse(circuit, qubits, b1, b2, b3):

    circuit.cx(qubits[b2], qubits[b3])
    circuit.cx(qubits[b1], qubits[b3])

#----------------------------------------------------------------------------------------------

def add_n(n, x, y):

    qr = QuantumRegister(1 + (3*n))
    cr = ClassicalRegister(1 + (3*n))

    circuit = QuantumCircuit(qr, cr)

    set_x, set_y, get_result = adder_n_get_set(circuit, qr, n)
    set_x(x)
    set_y(y)
    adder_n(circuit, qr, n, 0)
    circuit.measure(qr, cr)

    simulator = Aer.get_backend('qasm_simulator')
    result = execute(circuit, simulator, shots=1).result()
    counts = result.get_counts(circuit)

    r = get_result(counts)
    return r

def adder_n_get_set(circuit, qubits, n):

    # create list of qubits used to set the input values x and y
    x_bits = []
    y_bits = []
    for m in range(n):
        x_bits.append(1 + (3 * m))
        y_bits.append(2 + (3 * m))

    # list of classical bits to read the result
    r_bits = y_bits.copy()
    r_bits.append(3 * n)

    # generate and return lambdas to set the input x and y values and return the result
    set_x = lambda x: set_value(circuit, qubits, x, x_bits)
    set_y = lambda y: set_value(circuit, qubits, y, y_bits)
    get_result = lambda counts: get_value(counts, r_bits)

    return set_x, set_y, get_result

# adds an n bit adder to consecutive qubits in a circuit
# starting at qubit start_bit
def adder_n(circuit, qubits, n, start_bit):
# an nbit adder requires n x carry, (n-1) x carry-1, n x sum, 1 x cnot
# the adder is constructed as follows
#   n x carry starting at qubit: start_bit + 3m (m = 0..n-1)
#   1 x cnot at qubit: start_bit + 3n - 2
#   1 x sum at qubit: start_bit + 3(n-1)
#   n-1 x carry-1 and sum pair at qubit: start_bit + 3m (m = n-2..0)

    # add n x carry
    for m in range(n):
        i = start_bit + (3 * m)
        set_carry(circuit, qubits, i, i + 1, i + 2, i + 3)
        circuit.barrier()

    # add cnot
    i = start_bit + 3 * (n - 1) + 1
    circuit.cx(qubits[i], qubits[i + 1])
    circuit.barrier()

    # add sum and carry-1
    for m in reversed(range(n)):
        i = start_bit + (3 * m)
        # don't add carry first time
        if m < n - 1:
            set_carry_inverse(circuit, qubits, i, i + 1, i + 2, i + 3)
            circuit.barrier()

        set_sum(circuit, qubits, i, i + 1, i + 2)
        circuit.barrier()




