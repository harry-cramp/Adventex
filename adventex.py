# variable store - maps variables to names
variable_store = {}

VARIABLE_LABEL_QUERY = "query"
VARIABLE_LABEL_VALUE = "value"

def query_variable(query):
    return input(query)

def process_variables(lines):
    for line in lines:
        if line[0] != '\t':
            return
        words = line.split()
        variable_id = words[0]
        variable_value = line.partition(' ')[2]
        variable_store[variable_id] = variable_value[1:-2]

def printvf(text):
    formatted_text = ""
    for word in text.split():
        if word[0] == '%':
            key = word[1:]
            word = " " + variable_store[key]
        else:
            word = " " + word
        formatted_text += word
    print(formatted_text)

game_file = open("game.txt", "r")
data = game_file.readlines()
index = 0
for line in data:
    line = line.strip()
    print(line)
    if line == "TITLE":
        print(line.split()[1])
    elif line == "VARIABLES":
        print("LOADING VARIABLES")
        process_variables(data[index+1:])
    elif line == "GAME":
        break
    index = index + 1
# process situations
# process ending

    
