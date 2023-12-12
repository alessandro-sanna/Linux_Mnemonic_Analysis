from ghidra.program.model.listing import CodeUnitIterator, Instruction
import os


def get_only_opcodes(current_program):
	opcodes = []
	listing = current_program.getListing()
	code_units = listing.getCodeUnits(True)
	for code_unit in code_units:
		if isinstance(code_unit, Instruction):
			opcode_str = code_unit.toString().split(' ')[0]  # Ottieni solo la parte dell'opcode
			opcodes.append(opcode_str)
	return opcodes

currentProgram = getCurrentProgram()

only_opcodes = get_only_opcodes(currentProgram)

output_folder = "/home/asanna/.mnt/ELF_Dataset/encodingsBenignBatch/"
output_file_name = currentProgram.getExecutableSHA256() + ".csv"
output_file_name = os.path.join(output_folder, output_file_name)

with open(output_file_name, "w") as fwCsv:
	for opcode in only_opcodes:
		fwCsv.write(opcode + "\n")
