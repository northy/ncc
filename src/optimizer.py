import sys

dag = {}

def construct_leaf(leaf) :
    if leaf not in dag :
        dag[leaf] = {
            "name": [leaf],
            "in_degree": 0
        }

def construct_op(op, rd, rs1, rs2) :
    construct_leaf(rs1)
    construct_leaf(rs2)
    dag[rs1]["in_degree"] += 1
    dag[rs2]["in_degree"] += 1
    dag[rd] = {
        "op" : op,
        "in_degree": 0,
        "left": rs1,
        "right": rs2,
        "name": [rd]
    }

def construct_assign(rd, rs) :
    if rd.startswith('$') :
        dag[rd] = dag[rs]
        dag[rd]["name"].append(rd)
    else : #starts with %
        construct_leaf(rs)
        construct_leaf('0')
        dag[rs]["in_degree"] += 1
        dag['0']["in_degree"] += 1
        dag[rd] = {
            "op" : '+',
            "in_degree": 0,
            "left": rs,
            "right": '0',
            "name": [rd]
        }

def gv_name(item) :
    return '"\\'+", \\".join(dag[item]["name"])+("\\n"+dag[item]["op"] if "op" in dag[item] else "")+'"'

def to_gv(file) :
    file.write("graph dag {\n")
    for k,v in dag.items() :
        if "gv_visited" in v : continue
        v["gv_visited"] = True
        name = gv_name(k)
        if "op" in v :
            file.write(f'    {name} [shape=box]\n')
            file.write(f'    {name} -- {gv_name(v["left"])} [style=dotted]\n')
            file.write(f'    {name} -- {gv_name(v["right"])}\n')
    file.write("}\n")

def op_order() :
    L = []

    queue = []

    for k,v in dag.items() :
        if not(v["in_degree"]): queue.append(k)

    while len(queue)>0 :
        i = queue.pop(0)
        if "op" not in dag[i] or "order_visited" in dag[i] : continue

        dag[i]["order_visited"] = True
        L.append(i)

        dag[dag[i]["left"]]["in_degree"] -= 1
        if not(dag[dag[i]["left"]]["in_degree"]) : queue.append(dag[i]["left"])

        dag[dag[i]["right"]]["in_degree"] -= 1
        if not(dag[dag[i]["right"]]["in_degree"]) : queue.append(dag[i]["right"])

    L.reverse()
    return L

def to_ordered(file, order) :
    for oper in order :
        file.write(f"{dag[oper]['name'][0]} = {dag[oper]['left']} {dag[oper]['op']} {dag[oper]['right']}\n")
        for i in range(len(dag[oper]["name"])-1) :
            file.write(f"{dag[oper]['name'][i+1]} = {dag[oper]['name'][0]}\n")

def optimize(file, debug=False) :
    ic_f = open(file, "r")

    while (line:=ic_f.readline()) :
        line = line.split()
        
        if len(line)==5 : #rd = rs1 op rs2
            construct_op(line[3], line[0], line[2], line[4])
        elif len(line)==3 : #rd = rs
            construct_assign(line[0], line[2])
    
    ic_f.close()

    if debug :
        gv_f = open("dag.dot", "w+")
        to_gv(gv_f)
        gv_f.close()
    
    order = op_order()
    oic_f = open("out.oic", "w+")
    to_ordered(oic_f, order)
    oic_f.close()

if __name__=="__main__" :
    optimize("out.ic", True)
