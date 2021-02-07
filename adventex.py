# variable store - maps variables to names
variable_store = {}

situations = []

VARIABLE_LABEL_QUERY = "query"
VARIABLE_LABEL_VALUE = "value"

SITUATION_LABEL = "SITUATION"
SITUATION_ID = "ID"
SITUATION_DESCRIPTION = "DESCRIPTION"
SITUATION_OPTION_1 = "OPTION1"
SITUATION_OPTION_2 = "OPTION2"

END_LABEL = "END"

# class to hold situation information
class Situation:
    def __init__(self, id, description, option1, option1_instr, option2, option2_instr):
        self.id = id
        self.description = description
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
    option1 = ""
    option1_instructions = []
    option2 = ""
    option2_instructions = []
    loading_instructions = False
    logging_opt1_instr = True
    for line in situation_data:
        if loading_instructions and not line.startswith(SITUATION_OPTION_2):
            instruction = build_instruction(line[1:])
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
        elif demand == SITUATION_OPTION_1:
            option1 = remove_quotes(data)
            loading_instructions = True
        elif demand == SITUATION_OPTION_2:
            option2 = remove_quotes(data)
            logging_opt1_instr = False
            loading_instructions = True
    return Situation(event_id, description, option1, option1_instructions, option2, option2_instructions)

def build_instruction(data):
    return Instruction(data)

def query_variable(query):
    return input(query + " ")

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

def printvf(text):
    formatted_text = ""
    for word in text.split():
        if word[0] == '%':
            key = word[1:]
            word = variable_store[key] + " "
        else:
            word = word + " "
        formatted_text += word
    print(formatted_text)

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
        pass
    print("You chose: {0}".format(choice))

game_file = open("game.txt", "r")
data = game_file.readlines()
index = 0
is_game_data = False
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
            continue
        situation_data.append(line)
    index = index + 1

printvf("Your name is %NAME and you have %LIVES lives.")

for situation in situations:
    #print("Situation ID: " + str(situation.id))
    #print("Situation DESCRIPTION: " + situation.description)
    #print("Situation OPTION1: " + situation.option1)
    #print("Situation OPTION2: " + situation.option2)
    print_situation(situation)
    
