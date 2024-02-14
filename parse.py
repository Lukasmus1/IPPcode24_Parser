import sys
import os
import re
import xml.etree.ElementTree as ET

def regexVarMatch(string):
    return re.match(r"^(GF|LF|TF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$", string)

def regexSymMatch(string):
    return re.match(r"^(bool|nil|int|string)@.*$", string)

#Arg parser
args = sys.argv[1:]

if (len(args) == 1):
    if (args[0] == "--help"):
        print("ahojky")
        sys.exit(0)
    else:
        sys.exit(10)
elif (len(args) > 1):
    sys.exit(10)



# Vytvoření kořenového elementu
root = ET.Element("program language=\"IPPcode24\"")

# Vytvoření stromu z kořenového elementu
tree = ET.ElementTree(root)


#Kontrola hlavičky
if (sys.stdin.readline().strip() != ".IPPcode24"):
    print("Chybná hlavička")
    sys.exit(21)

orderInt = 1

for line in sys.stdin:
    #Ignorace prázdných řádků
    if (line == os.linesep):
        continue

    #Odstranění komentářů
    ind = line.find("#")
    if (ind != -1):
        line = line[:ind]

    #Rozdělení řádku na slova
    words = line.split()

    #https://youtu.be/iuZIeMIlCCM?si=H7W2MCPnHikY0JpT&t=932
    opcode = words[0].upper()
    match opcode:
        case "MOVE" | "INT2CHAR" | "STRLEN" | "TYPE":
            if (len(words) != 3):
                print("Chybný počet argumentů")
                sys.exit(23)

            if (not regexVarMatch(words[1])):
                print("Chybný formát argumentu")
                sys.exit(23)

            if (not regexVarMatch(words[2])):
                print("Chybný formát argumentu")
                sys.exit(23)

            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            content = ET.SubElement(el, "arg1", type="var")
            content.text = words[1]
            content = ET.SubElement(el, "arg2", type="var")
            content.text = words[2]

        case "CREATEFRAME" | "PUSHFRAME" | "POPFRAME" | "RETURN" | "BREAK":
            if (len(words) != 1):
                print("Chybný počet argumentů")
                sys.exit(23)
            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)


        case "DEFVAR" | "POPS":
            if (len(words) != 2):
                print("Chybný počet argumentů")
                sys.exit(23)

            if (not regexVarMatch(words[1])):
                print("Chybný formát argumentu")
                sys.exit(23)

            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            content = ET.SubElement(el, "arg1", type="var")
            content.text = words[1]

        case _:
            print("Neznámý opcode")
            sys.exit(22)
    
    orderInt = orderInt + 1

        
ET.indent(tree, space="    ")
tree.write("output.xml", encoding="UTF-8", xml_declaration=True)

