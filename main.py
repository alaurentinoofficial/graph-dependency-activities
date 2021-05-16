from node import PythonNode, DelayNode
from pipeline import Pipeline

if __name__ == "__main__":
    with Pipeline("Test flow") as pipe:
        a = PythonNode("A", "...", lambda: print("Isso foi a atividade A"))
        b = PythonNode("B", "...", lambda: print("Isso foi a atividade B"))
        c = DelayNode("C", "...", 15)
        d = DelayNode("D", "...", 10)
        e = PythonNode("E", "...", lambda: print("Só executa depois de todos os outros"))

        # A - D - E
        #       /
        # C - B
        a >> d
        c >> b
        e << [d, b]

        print(a.name.value + ": ", list(map(lambda x: x.name.value, a.predecessors)), ">>", list(map(lambda x: x.name.value, a.sucessors)))
        print(b.name.value + ": ", list(map(lambda x: x.name.value, b.predecessors)), ">>", list(map(lambda x: x.name.value, b.sucessors)))
        print(c.name.value + ": ", list(map(lambda x: x.name.value, c.predecessors)), ">>", list(map(lambda x: x.name.value, c.sucessors)))
        print(d.name.value + ": ", list(map(lambda x: x.name.value, d.predecessors)), ">>", list(map(lambda x: x.name.value, d.sucessors)))
        print(e.name.value + ": ", list(map(lambda x: x.name.value, e.predecessors)), ">>", list(map(lambda x: x.name.value, e.sucessors)))