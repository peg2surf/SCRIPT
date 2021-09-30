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


def flow_update() -> None:
    """
    Every cycle, this function updates the values in network based on the changes
    inacted. Affect only globals so no argument or outputs.
    """
    global network
    global path
    global flow
    global orb
    for x in network:
        if not network[x][2]:
            network[x][0] = flow * (x in path)
        network[x][1] = bool(network[x][0] and network[x][1])
    network[path[-1]][1] = orb | network[path[-1]][1]


def node_flow_set(vars: list, flow: int) -> None:
    """
    'SET's a node so it's flow is unchagable regarless of path
    or any other factor. Used to simulate a another ORG.
    """
    for x in vars:
        network[y][0] = flow
        network[y][2] = True


def connect(origin: str, vars: list) -> None:
    """
    Connects an array nodes to a
    """
    if origin not in network.keys():
        conections[origin] = []
    for x in vars:
        if x not in conections.keys():
            conections[x] = []
        conections[origin].append(x)
    for x in conections.keys():
        network[x] = [0, False, False]


def translate(text: str) -> None:
    global instructions
    instructions = [
        list(filter(None, map(lambda x: x.upper(),
             x.split('//')[0].split('\\')[0].split(' '))))
        for x in text.strip().replace(', ', ',').replace(' ,', ',').replace('  ', '').replace('\n', ';').split(';')
        if x != '' and x[:2] != '//' and x[:2] != '\\'
    ]


def run(code: str, instructions_on: bool = False, endstate: bool = False, visualize: bool = False) -> None:
    global network
    global instructions
    global path
    global orb
    global flow
    global compare

    translate(code)

    data: int = instructions.index(['SECTION', '.DATA:'])
    start: int = instructions.index(['_START:'])

    for x in range(data, start):
        if instructions_on:
            print(instructions[x])
        if "->" in instructions[x]:
            clone = instructions[x][:instructions[x].index(
                '->')] + instructions[x][instructions[x].index('->') + 1].split(',')
            connect(clone[0], clone[1:])
        if instructions[x][0] == "SET":
            for y in instructions[x][1].split(','):
                network[y][0] = int(instructions[x][2])
                network[y][2] = True
    x = start
    while x < len(instructions):
        if instructions_on:
            print(instructions[x])
        if instructions[x][0] == "CRT":
            print(not(network[path[-1]][1]))
            orb = not(network[path[-1]][1])
        elif instructions[x][0] == "FLW":
            flow = int(instructions[x][1])
        elif instructions[x][0] == "PTH":
            path = []
            if len(instructions[x]) != 1:
                path = ['ORG'] + instructions[x][1].split(',')
        elif instructions[x][0] == "RLS":
            orb = False
        elif instructions[x][0] == "CMP":
            compare = orb
        elif instructions[x][0] == "JMP":
            x = instructions.index([instructions[x][1] + ':'])
        elif instructions[x][0] == "JPT" and compare:
            x = instructions.index([instructions[x][1] + ':'])
        elif instructions[x][0] == "JPF" and not compare:
            x = instructions.index([instructions[x][1] + ':'])
        elif instructions[x][0] == "SET":
            node_flow_set(instructions[x][1].split(','), instructions[x][2])
        elif instructions[x][0] == "END":
            break
        flow_update()
        x += 1
    if endstate:
        print(f"""conections: {conections} \nnetwork : {network} 
        \npath : {path} \norb : {orb} \nflow : {flow} \ncompare : {compare}""")
    vizualize_conections(visualize=visualize)


def filetostring(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()


def vizualize_conections(strict: bool = True, visualize: bool = False) -> None:
    global network
    from graphviz import Graph, Source
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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-i", "--instructions", action="store_true",
                        help="Print instructions from interpreter")
    parser.add_argument("-e", "--endstate", action="store_true",
                        help="Print all states at end of run")
    parser.add_argument("-v", "--visualize", action="store_true",
                        help="Vizualize Graph at end")
    args = parser.parse_args()

    run(code=filetostring(args.filename), instructions_on=args.instructions,
        endstate=args.endstate, visualize=args.visualize)


if __name__ == "__main__":
    main()
