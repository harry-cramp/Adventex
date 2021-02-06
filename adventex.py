# variable store - maps variables to names
variable_store = {}

VARIABLE_LABEL_QUERY = "query"
VARIABLE_LABEL_VALUE = "value"

def query_variable(query):
    return input(query)

def remove_quotes(text):
    return text[1:-2]

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

game_file = open("game.txt", "r")
data = game_file.readlines()
index = 0
for line in data:
    line = line.strip()
    if line == "TITLE":
        print(line.split()[1])
    elif line == "VARIABLES":
        process_variables(data[index+1:])
    elif line == "GAME":
        break
    index = index + 1
# process situations
# process ending

printvf("Your name is %NAME and you have %LIVES lives.")
    
