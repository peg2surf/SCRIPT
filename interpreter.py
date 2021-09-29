# The network is the absractions of the connections of circuits
global network
# The instructions of the code
global instructions
# Current path of the code
global path
# If there currently is a orb
global orb
# The flow of Origin
global flow
# The current cached compare value
global compare

conections: dict = {}
network: dict = {}
instructions: list = []
path: list = ['ORG']
orb: bool = False
flow: int = 0
compare: int = None

#FLOW, ORB, SET


def flow_update():
    global network
    global path
    global flow
    global orb
    for x in network:
        if not network[x][2]:
            network[x][0] = flow * (x in path)
        network[x][1] = bool(network[x][0] and network[x][1])
    network[path[-1]][1] = orb | network[path[-1]][1]


def val_set(vars: list, flow: int):
    for x in vars:
        network[y][0] = flow
        network[y][2] = True


def connect(vars):
    if vars[0] not in network.keys():
        conections[vars[0]] = []
    for x in vars[1:]:
        if x not in conections.keys():
            conections[x] = []
        conections[vars[0]].append(x)
    for x in conections.keys():
        network[x] = [0, False, False]


def transl(text: str):
    global instructions
    instructions = [
        list(filter(None, map(lambda x: x.upper(),
             x.split('//')[0].split('\\')[0].split(' '))))
        for x in text.strip().replace(', ', ',').replace(' ,', ',').replace('  ', '').replace('\n', ';').split(';')
        if x != '' and x[:2] != '//' and x[:2] != '\\'
    ]


def run(code: str):
    global network
    global instructions
    global path
    global orb
    global flow
    global compare
    transl(code)
    data: int = instructions.index(['SECTION', '.DATA:'])
    start: int = instructions.index(['_START:'])

    for x in range(data, start):
        print(instructions[x])
        if "->" in instructions[x]:
            clone = instructions[x][:instructions[x].index(
                '->')] + instructions[x][instructions[x].index('->') + 1].split(',')
            connect(clone)
        if instructions[x][0] == "SET":
            for y in instructions[x][1].split(','):
                network[y][0] = int(instructions[x][2])
                network[y][2] = True
    x = start
    while x < len(instructions):
        print(instructions[x])
        if instructions[x][0] == "CRT":
            orb = not(network[path[-1]][1])
            #print(f'Orb: {orb}')
        if instructions[x][0] == "FLW":
            flow = int(instructions[x][1])
        if instructions[x][0] == "PTH":
            path = []
            if len(instructions[x]) != 1:
                path = ['ORG'] + instructions[x][1].split(',')
            # print(path)
        if instructions[x][0] == "RLS":
            orb = False
            #print(f'Orb: {orb}')
        if instructions[x][0] == "CMP":
            compare = orb
            #print(f'Comp: {orb}')
        if instructions[x][0] == "JMP":
            x = instructions.index([instructions[x][1] + ':'])
        if instructions[x][0] == "JPT" and compare:
            x = instructions.index([instructions[x][1] + ':'])
        if instructions[x][0] == "JPF" and not compare:
            x = instructions.index([instructions[x][1] + ':'])
        if instructions[x][0] == "SET":
            val_set(instructions[x][1].split(','), instructions[x][2])
        if instructions[x][0] == "END":
            break
        flow_update()
        x += 1


def filetostring(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()


def viz_conections(strict: bool = True):
    from graphviz import Graph, Digraph, Source
    g = Graph(strict=strict)
    g.node('ORG', color='purple')
    for x in conections.keys():
        if network[x][1]:
            g.node(str(x), color='blue')
        for y in conections[x]:
            g.edge(str(x), str(y),
                   color=('red' if y in path else 'black'))
    s = Source(g, filename="test.gv", format="png")
    s.view()


def main():
    run(filetostring("SCRIPT\ORGATE"))
    print(conections)
    print(network)
    viz_conections()


if __name__ == "__main__":
    main()
