# riscv_assembler.py
import re

# RISC-V instruction encoding
OPCODES = {
    'add': 0b0110011,
    'addi': 0b0010011,
    'sub': 0b0110011,
    'and': 0b0110011,
    'or': 0b0110011,
    'xor': 0b0110011,
    'sll': 0b0110011,
    'srl': 0b0110011,
    'sra': 0b0110011,
    'stl': 0b0110011,
    'stlu': 0b0110011,
    'andi': 0b0010011,
    'ori': 0b0010011,
    'xori': 0b0010011,
    'slti': 0b0010011,
    'sltiu': 0b0010011,
    'slli': 0b0010011,
    'srli': 0b0010011,
    'srai': 0b0010011,
    'lui': 0b0110111,
    'auipc': 0b0010111,
}

FUNCT3 = {
    'add': 0b000,
    'sub': 0b000,
    'and': 0b111,
    'or': 0b110,
    'xor': 0b100,
    'sll': 0b001,
    'srl': 0b101,
    'sra': 0b101,
    'stl': 0b010,
    'stlu': 0b011,
    'addi': 0b000,
    'andi': 0b111,
    'ori': 0b110,
    'xori': 0b100,
    'slti': 0b010,
    'sltiu': 0b011,
    'slli': 0b001,
    'srli': 0b101,
    'srai': 0b101,
}

FUNCT7 = {
    'add': 0b0000000,
    'sub': 0b0100000,
    'and': 0b0000000,
    'or': 0b0000000,
    'xor': 0b0000000,
    'sll': 0b0000000,
    'srl': 0b0000000,
    'sra': 0b0100000,
    'stl': 0b0000000,
    'stlu': 0b0000000,
}

REGISTER_MAP = {
    'x0': 0, 'x1': 1, 'x2': 2, 'x3': 3, 'x4': 4, 'x5': 5, 'x6': 6, 'x7': 7,
    'x8': 8, 'x9': 9, 'x10': 10, 'x11': 11, 'x12': 12, 'x13': 13, 'x14': 14,
    'x15': 15, 'x16': 16, 'x17': 17, 'x18': 18, 'x19': 19, 'x20': 20, 'x21': 21,
    'x22': 22, 'x23': 23, 'x24': 24, 'x25': 25, 'x26': 26, 'x27': 27, 'x28': 28,
    'x29': 29, 'x30': 30, 'x31': 31
}

def encode_r_type(instr, rd, rs1, rs2):
    opcode = OPCODES[instr]
    funct3 = FUNCT3[instr]
    funct7 = FUNCT7[instr]
    rd = REGISTER_MAP[rd]
    rs1 = REGISTER_MAP[rs1]
    rs2 = REGISTER_MAP[rs2]
    encoding = (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
    return encoding

def encode_i_type(instr, rd, rs1, imm):
    opcode = OPCODES[instr]
    funct3 = FUNCT3[instr]
    rd = REGISTER_MAP[rd]
    rs1 = REGISTER_MAP[rs1]
    imm = int(imm) & 0xFFF  # Immediate is 12 bits
    encoding = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
    return encoding

def encode_u_type(instr, rd, imm):
    opcode = OPCODES[instr]
    rd = REGISTER_MAP[rd]
    if imm.startswith('0x'):
        imm = int(imm, 16)  # Parse hexadecimal immediate
    else:
        imm = int(imm)  # Parse decimal immediate
    imm = imm & 0xFFFFF  # Immediate is 20 bits
    encoding = (imm << 12) | (rd << 7) | opcode
    return encoding

def parse_instruction(line):
    parts = line.split()
    instr = parts[0]
    if instr in OPCODES:
        if instr in FUNCT7:
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            return encode_r_type(instr, rd, rs1, rs2)
        elif instr in FUNCT3:
            rd, rs1, imm = parts[1], parts[2], parts[3]
            return encode_i_type(instr, rd, rs1, imm)
        elif instr in ['lui', 'auipc']:
            rd, imm = parts[1], parts[2]
            return encode_u_type(instr, rd, imm)
    return None

def main():
    input_file = 'assembly_instructions.txt'
    output_file = 'riscv_binary.txt'

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            encoding = parse_instruction(line)
            if encoding is not None:
                outfile.write(f'{encoding:032b}\n')

if __name__ == '__main__':
    main()
