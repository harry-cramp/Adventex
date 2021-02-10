# Adventex
A game engine for choice-based Text Adventure games

## Writing an Adventex Text Adventure game
Adventex games are structured in two main parts:
- `VARIABLES`: Setting and processing the game variables
- `SITUATIONS`: The game is split into situations which are events where the user can choose what to do

### Processing variables
In the game file, the `VARIABLES` section defines the variables in the game, e.g.:
```
VARIABLES
  NAME query="Type your name:"
  LIVES value="3"
```
Will set the variable %LIVES to 3 and will query the user to input a value for %NAME using the specified query.

### Creating situations
Situations are comprised of five parts:
- `ID`: The unique numerical identifier for this situation
- `DESCRIPTION`: The text printed on the screen describing to the user what is happening
- `FALLBACK`: The text printed on the screen when the user types a non-numerical value as input
- `OPTION1`, `OPTION2`: The two choices the user is given

### Option path instructions
The options elements have their own elements called instructions which are executed when that path is taken.

Here are all the possible instructions:
- `PRINT "<text>"`: Prints the specified text to the screen
- `INC <VARIABLE> <value>`: Increment the specified variable by the specified amount
- `DEC <VARIABLE> <value>`: Decrement the specified variable by the specified amount
- `JUMP <situation id>`: Jump to the situation specified by its unique ID
