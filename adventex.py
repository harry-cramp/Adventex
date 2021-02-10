# variable store - maps variables to names
variable_store = {}

situations = []
# instructions to execute when game ends
end_instr = []

# Reserved variable names
RESERVED_VAR_INPUT = "INPUT"

VARIABLE_LABEL_QUERY = "query"
VARIABLE_LABEL_VALUE = "value"

SITUATION_LABEL = "SITUATION"
SITUATION_ID = "ID"
SITUATION_DESCRIPTION = "DESCRIPTION"
SITUATION_FALLBACK = "FALLBACK"
SITUATION_OPTION_1 = "OPTION1"
SITUATION_OPTION_2 = "OPTION2"

INSTRUCTION_PRINT = "PRINT"
INSTRUCTION_INC = "INC"
INSTRUCTION_DEC = "DEC"
INSTRUCTION_JUMP = "JUMP"

END_LABEL = "END"

# class to hold situation information
class Situation:
    def __init__(self, id, description, fallback, option1, option1_instr, option2, option2_instr):
        self.id = id
        self.description = description
        self.fallback = fallback
        self.option1 = option1
        self.option1_instr = option1_instr
        self.option2 = option2
        self.option2_instr = option2_instr

# class to hold game instruction information
class Instruction:
    def __init__(self, instruction):
        self.instruction = instruction
        self.opcode = instruction.split(" ")[0]

def build_situation(situation_data):
    event_id = 0
    description = ""
    fallback = ""
    option1 = ""
    option1_instructions = []
    option2 = ""
    option2_instructions = []
    loading_instructions = False
    logging_opt1_instr = True
    for line in situation_data:
        if loading_instructions and not line.startswith(SITUATION_OPTION_2):
            instruction = build_instruction(line)
            if logging_opt1_instr == True:
                option1_instructions.append(instruction)
            else:
                option2_instructions.append(instruction)
            continue
        demand = line.partition(" ")[0]
        data = line.partition(" ")[2]
        if demand == SITUATION_ID:
            event_id = int(data)
        elif demand == SITUATION_DESCRIPTION:
            description = remove_quotes(data)
        elif demand == SITUATION_FALLBACK:
            fallback = remove_quotes(data)
        elif demand == SITUATION_OPTION_1:
            option1 = remove_quotes(data)
            loading_instructions = True
        elif demand == SITUATION_OPTION_2:
            option2 = remove_quotes(data)
            logging_opt1_instr = False
            loading_instructions = True
    return Situation(event_id, description, fallback, option1, option1_instructions, option2, option2_instructions)

def get_situation(jump_id):
    for situation in situations:
        if int(situation.id) == int(jump_id):
            return situation

def build_instruction(data):
    return Instruction(data)

def query_variable(query):
    printvf(query)
    return input("")

def remove_quotes(text):
    return text.strip().replace('"', '')

def process_variables(lines):
    for line in lines:
        if line[0] != '\t':
            return
        words = line.split()
        variable_id = words[0]
        variable_value = line.partition(' ')[2]
        components = variable_value.split('=')
        label = components[0]
        if label == VARIABLE_LABEL_QUERY:
            variable_store[variable_id] = query_variable(remove_quotes(variable_value.split('=')[1]))
        elif label == VARIABLE_LABEL_VALUE:
            variable_store[variable_id] = remove_quotes(components[1])

def increment_variable(variable_id, amount):
    variable_store[variable_id] = int(variable_store[variable_id]) + amount

def decrement_variable(variable_id, amount):
    variable_store[variable_id] = int(variable_store[variable_id]) - amount

def process_instruction(instruction):
    command = instruction.opcode
    operand = instruction.instruction.replace(command + " ", "")
    if command == INSTRUCTION_PRINT:
        printvf(remove_quotes(operand))
    elif command == INSTRUCTION_INC:
        elements = operand.split(" ")
        variable_id = elements[0]
        value = int(elements[1])
        increment_variable(variable_id, value)
    elif command == INSTRUCTION_DEC:
        elements = operand.split(" ")
        variable_id = elements[0]
        value = int(elements[1])
        decrement_variable(variable_id, value)
    elif command == INSTRUCTION_JUMP:
        print_situation(get_situation(operand))
    elif command == END_LABEL:
        execute_path(end_instr)

def execute_path(instructions):
    for instruction in instructions:
        process_instruction(instruction)
    
def printvf(text):
    for variable_id in variable_store:
        text = text.replace("%" + variable_id, str(variable_store[variable_id]))
    print(text)

def print_situation(situation):
    printvf(situation.description)
    print("1 to {0} or 2 to {1}".format(situation.option1.upper(), situation.option2.upper()))
    choice = input()
    is_int = True
    try:
        choice = int(choice)
    except:
        # input not integer
        is_int = False
        # set reserved variable %INPUT to user's input
        variable_store[RESERVED_VAR_INPUT] = choice
        printvf(situation.fallback)
        print_situation(situation)
        pass

    if is_int == True:
        if choice == 1:
            execute_path(situation.option1_instr)
        else:
            execute_path(situation.option2_instr)

game_file = open("game.txt", "r")
data = game_file.readlines()
index = 0
is_game_data = False
is_end_data = False
situation_data = []
for line in data:
    line = line.strip()
    if line == "TITLE":
        print(line.split()[1])
    elif line == "VARIABLES":
        process_variables(data[index+1:])
    elif line == "GAME":
        is_game_data = True
    elif is_game_data == True:
        line = line.strip()
        if line == SITUATION_LABEL:
            if not situation_data:
                continue
            else:
                situations.append(build_situation(situation_data))
                situation_data = []
        elif line == END_LABEL:
            is_game_data = False
            is_end_data = True
            continue
        situation_data.append(line)
    elif is_end_data == True:
        end_instr.append(build_instruction(line))
    index = index + 1

# begin game with first situation
print_situation(situations[0])
    
