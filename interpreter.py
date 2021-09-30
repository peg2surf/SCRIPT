"""
Author: Pablo Eduardo Ghezzi Barton
Year: 2021
Language: Python/English
"""

"""
KNT = 3
ENH = 4
BC = 5
CNJ = 6
MNP = 7
TRS = 8
"""

"""
Const for instructions and format keys.
Can be changed but probably should not.
"""

INS_NEWLINE = ';'
INS_DIVIDE = ','
INS_COMMENT = ['\\', '//']

INS_DATA = ['SECTION', '.DATA:']
INS_START = ['_START:']

INS_CONNECT = '->'
INS_SET = "SET"
INS_UNSET = "UNS"

"""
TOADD?: Beta to test in master
Origin Shift = "@[New Origin]"
Set Path = "SET PTH"
Unset = "UST [var]"
"""

INS_ORIGIN = '@'

INS_CREATE = "CRT"
INS_FLOW = "FLW"
INS_SPIN = "SPIN"
INS_PATH = "PTH"
INS_RELEASE = "RLS"
INS_COMPARE = "CMP"
INS_JUMP = "JMP"
INS_JUMPTRUE = "JPT"
INS_JUMPFALSE = "JPF"
INS_END = "END"

FLOW_LOC = 0
ORB_LOC = 1
SPIN_LOC = 2
SET_LOC = 3

"""
Creates globals and set their default values
- instructions variable used to store the formated instructions
- network used to store the current state of each node
- conections used to store the connections between each node
- path the current path of the ORGIN
- orb the current state of the ORB
- flow the current flow of the ORGIN
- compare the current stached value of CMP
"""

global instructions
global network
global conections
global path
global orb
global flow
global compare

origin = 'ORG'
instructions: list = []
network: dict = {}
conections: dict = {}
path: list = [origin]
orb: bool = False
flow: int = 0
spin: int = 0
compare: int = None


def cycle() -> None:
    """
    Every cycle, this function updates the values in network based on the changes
    inacted. 
    \nAffect only globals so no argument or outputs.
    """
    global network
    global path
    global flow
    global orb

    for x in network:
        if not network[x][SET_LOC]:
            network[x][FLOW_LOC] = flow * (x in path)
        network[x][ORB_LOC] = bool(
            network[x][FLOW_LOC] and network[x][ORB_LOC])
    network[path[-1]][ORB_LOC] = orb | network[path[-1]][ORB_LOC]
    if network[path[-1]][ORB_LOC]:
        network[path[-1]][SPIN_LOC] = spin


def origin_set(new_origin: str) -> None:
    """
    Sets new origin to emulate new origin
    \nnew_origin origin to replace old

    NOTE: This does not replace the old path. To reset use `PTH`
    """
    global origin
    origin = new_origin


def connect(origin: str, vars: list) -> None:
    """
    Connects an origin to array nodes to array of node in a
    one direction fashion.
    \norigin the origin for all the connections
    \nvars all the items connected to origin
    """
    global network
    global conections
    if origin not in network.keys():
        conections[origin] = []
    for x in vars:
        if x not in conections.keys():
            conections[x] = []
        conections[origin].append(x)
    for x in conections.keys():
        # [flow, orb?, set?]
        network[x] = [0, False, 0, False]


def node_flow_set(vars: list, flow: int = 1, setted: bool = True) -> None:
    """
    'SET's a node so it's flow is unchagable regarless of path
    or any other factor. Used to simulate a another ORG.
    \nvars all item to set flow
    \nflow the flow to set the items in var
    """
    global network
    if vars == [INS_PATH]:
        global path
        for x in path:
            network[x][FLOW_LOC] = flow
            network[x][SET_LOC] = setted
    for x in vars:
        network[x][FLOW_LOC] = flow
        network[x][SET_LOC] = setted


def node_flow_unset(vars: list) -> None:
    """
    'UST's a node so it's set property is removed
    \nvars all item to set flow
    """
    global network
    if vars == [INS_PATH]:
        global path
        for x in path:
            network[x][SET_LOC] = False
    for x in vars:
        network[x][SET_LOC] = False


def create() -> None:
    """
    Runs create command
    """
    global orb
    orb = not(network[path[-1]][1])


def flow_update(new_flow: int) -> None:
    """
    Runs release command
    """
    global flow
    flow = new_flow


def path_update(new_path: list) -> None:
    """
    Runs release command
    """
    global path
    path = []
    if new_path != []:
        path = [origin] + new_path


def release() -> None:
    """
    Runs release command
    """
    global orb
    orb = False


def compare_update() -> None:
    """
    Runs compare command
    """
    global compare
    global orb
    compare = orb


# ADD JUMP?


def translate(text: str) -> None:
    """
    Translates raw text into arrays readable by the iterpreter.
    Need efficiency tweeks.
    \ntext rawcode of type .ob or text file
    """
    global instructions
    instructions = [
        list(filter(None, map(lambda x: x.upper(),
             x.split(INS_COMMENT[0])[0].split(INS_COMMENT[1])[0].split(' '))))
        for x in text.strip().replace(', ', INS_DIVIDE).replace(' ,', INS_DIVIDE).replace('  ', '').replace(INS_ORIGIN, INS_ORIGIN + ' ').replace('\n', INS_NEWLINE).split(INS_NEWLINE)
        if x != '' and x[:2] != INS_COMMENT[0] and x[:2] != INS_COMMENT[1]
    ]


def run(code: str, instructions_on: bool = False, endstate: bool = False, visualize: bool = False) -> None:
    """
    Runs formated instructions
    \ncode formated instrunctions
    \ninstructions_on (default False) prints all instructions they are proceesed by the interpreter
    \nendstate (default False) print all globals used
    \nvisualiz (default False) use globals to make a visual graph of the endstate
    """
    global network
    global instructions
    global path
    global orb
    global flow
    global compare

    translate(code)

    data: int = instructions.index(INS_DATA)
    start: int = instructions.index(INS_START)

    for x in range(data, start):
        if instructions_on:
            print(instructions[x])
        if INS_CONNECT in instructions[x]:
            clone = instructions[x][:instructions[x].index(
                INS_CONNECT)] + instructions[x][instructions[x].index(INS_CONNECT) + 1].split(',')
            connect(clone[0], clone[1:])
        elif instructions[x][0] == INS_SET:
            node_flow_set(instructions[x][1].split(','), instructions[x][2])
        elif instructions[x][0] == INS_UNSET:
            node_flow_set(vars=instructions[x][1].split(
                ','), flow=0, setted=False)
    x = start
    while x < len(instructions):
        if instructions_on:
            print(instructions[x])
        if instructions[x][0] == INS_CREATE:
            create()
        elif instructions[x][0] == INS_FLOW:
            flow_update(new_flow=int(instructions[x][1]))
        elif instructions[x][0] == INS_PATH:
            path_update(new_path=instructions[x][1].split(INS_DIVIDE))
        elif instructions[x][0] == INS_RELEASE:
            release()
        elif instructions[x][0] == INS_COMPARE:
            compare_update()
        elif instructions[x][0] == INS_JUMP:
            x = instructions.index([instructions[x][1] + ':'])
        elif instructions[x][0] == INS_JUMPTRUE and compare:
            x = instructions.index([instructions[x][1] + ':'])
        elif instructions[x][0] == INS_JUMPFALSE and not compare:
            x = instructions.index([instructions[x][1] + ':'])
        elif instructions[x][0] == INS_SET:
            node_flow_set(vars=instructions[x][1].split(
                ','), flow=instructions[x][2])
        elif instructions[x][0] == INS_UNSET:
            node_flow_set(vars=instructions[x][1].split(
                ','), flow=0, setted=False)
        elif instructions[x][0] == INS_END:
            break
        cycle()
        x += 1
    if endstate:
        print(
            f"conections: {conections} \nnetwork : {network} \npath : {path}" +
            f"\norb : {orb} \nflow : {flow} \ncompare : {compare}")
    if visualize:
        vizualize_conections(visualize=visualize)


def filetostring(filename: str) -> str:
    """
    Return a str of the entire contents of a file
    \nfilename the name of file to read
    """
    with open(filename, 'r') as file:
        return file.read()


def vizualize_conections(filename: str = 'out', strict: bool = True, visualize: bool = False) -> None:
    """
    Creates a a .gv file based on the endstate global network
    \nfilename (default 'out') the name of .gv created
    \nstrict (default True) will not repeate connections if they exist
    \nvisualize (default False) will open a .png of .gv file to visualize 
    """
    global network
    from graphviz import Graph, Source
    g = Graph(strict=strict)
    g.node(origin, color='purple')
    for x in conections.keys():
        if network[x][1]:
            g.node(str(x), color='blue')
        for y in conections[x]:
            g.edge(str(x), str(y),
                   color=('red' if y in path else 'black'))
    s = Source(g, filename=filename, format="png")
    if visualize:
        s.view()


def main():
    """
    main function, runs when dirrectly run from cmd prompt
    accepts cmd arguments
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-i", "--instructions", action="store_true",
                        help="print instructions from interpreter")
    parser.add_argument("-e", "--endstate", action="store_true",
                        help="print all states at end of run")
    parser.add_argument("-v", "--visualize", action="store_true",
                        help="vizualize Graph at end")
    args = parser.parse_args()

    run(code=filetostring(args.filename), instructions_on=args.instructions,
        endstate=args.endstate, visualize=args.visualize)


if __name__ == "__main__":
    main()
