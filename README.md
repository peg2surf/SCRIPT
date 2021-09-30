# SCRIPT

Based on assembly, SCRIPT has no variables and is based on simple commands,
using instead a network of nodes and paths. You can create and release orbs.
While a orb is connected to the ORIGIN it will exist. If it is release it can
only continue existing if it it powered by the node it currently resides.
If node does not have a flow (e.i a flow of 0) then the orb disapears.
Two orbs cannot exist in the same node so the newest orb will be destroyed if
it attempts to be created.

## Basicss

### section .data

This creates the network on a basis of one to many.
You can also set the flow of points so they will always remain unchanged. ex:

- `[VAR1] -> [VAR]` creates a connection between `VAR1` and all values in `VAR`

- `SET [VAR1] [VAL]` will create a constant value of flow at `VAR1` by `VAL`

### .start

This where the code really starts and where the logic occurs.

### Commands

- `[VAR1] -> [VAR2]` creates and connects VAR1 and VAR2. VAR2 can be multiple. Can only be used in `section .data`
- `SET [VAR1] [VAL]` creates and sets a constant value of flow at `VAR1` by `VAL`
- `UST [VAR1]` unsets the VAR1 if set

- `@ [VAR1]` changes the origin to `VAR1`

- `CRT` creates a orb at the end of the path
- `FLW [VAL]` sets the value of the flow with `VAL`
- `PTH [VARS]` sets the path with `VARS`. Leave empty to reset to origin
- `RLS` releases the current orb from the end of the path
- `CMP` saves the current value of wheter the orb exist or not
- `JMP [NAME]` jumps to a certain function denominated by `[NAME]:`
- `JPT [NAME]` same as jump but only if CMP was true
- `JPF [NAME]` same as jump but only if CMP was false
- `END` ends code regardless of current line
- `;` can be used to end lines but is not nessecary if newlines are used

### Example

```Assembly
//ANDGATE

\\Comment work like this
//or like this

section .data:
  ORG -> VAR1, VAR2, VAR3

  SET VAR1 1

_start:
  PTH VAR1
  CRT
  RLS
  CRT
  CMP
  JPT False
  RLS
  PTH VAR2
  CRT
  RLS
  CRT
  CMP
  JPT False
  RLS
  JMP True

False:
  RLS
  PTH VAR3
  END

True:
  PTH VAR3
  CRT
  FLW 1
  END
```
