import sys
import os
import re
import xml.etree.ElementTree as ET

def regexVarMatch(string):
    isVar = False
    words = string.split("@")
    var = re.match(r"^(GF|LF|TF)", words[0])
    var = var and regexLabelMatch(words[1])
    if (not var):
        arg = string.split("@")
        match arg[0]:
            case "int":
                return re.match(r"^[-+]?[0-9]+$", arg[1]), isVar
            case "bool":
                return re.match(r"^(true|false)$", arg[1]), isVar
            case "string":
                return re.match(r"^([^\s#]|\\[0-9]{3})*$", arg[1]), isVar
            case "nil":
                return re.match(r"^nil$", arg[1]), isVar
            case _:
                return False, isVar
    isVar = True
    return True, isVar

def regexLabelMatch(string):
    return re.match(r"^[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$", string)

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
for line in sys.stdin:
    ind = line.find("#")
    if (ind != -1):
        line = line[:ind]

    line = line.strip()
    if(len(line) == 0):
        continue

    if (line == ".IPPcode24"):
        break
    else:
        print("Chybná hlavička")
        sys.exit(21)


orderInt = 1

for line in sys.stdin:
    #Odstranění komentářů
    ind = line.find("#")
    if (ind != -1):
        line = line[:ind]

    #Ignorace prázdných řádků
    if (line == os.linesep or len(line.strip()) == 0):
        continue

    #Rozdělení řádku na slova
    words = line.split()

    #https://youtu.be/iuZIeMIlCCM?si=H7W2MCPnHikY0JpT&t=932
    opcode = words[0].upper()
    match opcode:
        case "MOVE" | "INT2CHAR" | "STRLEN" | "TYPE":
            if (len(words) != 3):
                print("Chybný počet argumentů")
                sys.exit(23)

            res, isVar = regexVarMatch(words[1])
            if (not res):
                print("Chybný formát argumentu")
                sys.exit(23)

            res2, isVar2 = regexVarMatch(words[2])
            if (not regexVarMatch(words[2])):
                print("Chybný formát argumentu")
                sys.exit(23)

            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            if (isVar):
                content = ET.SubElement(el, "arg1", type="var")
            else:
                content = ET.SubElement(el, "arg1", type=words[1].split("@")[0])
            content.text = words[1]

            if (isVar2):
                content = ET.SubElement(el, "arg2", type="var")
            else:
                content = ET.SubElement(el, "arg2", type=words[2].split("@")[0])
            content.text = words[2]

        case "CREATEFRAME" | "PUSHFRAME" | "POPFRAME" | "RETURN" | "BREAK":
            if (len(words) != 1):
                print("Chybný počet argumentů")
                sys.exit(23)
            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)


        case "DEFVAR" | "POPS" | "PUSHS" | "WRITE" | "EXIT" | "DPRINT":
            if (len(words) != 2):
                print("Chybný počet argumentů")
                sys.exit(23)

            res, isVar = regexVarMatch(words[1])
            if (not res):
                print("Chybný formát argumentu")
                sys.exit(23)
            
            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            if (isVar):    
                content = ET.SubElement(el, "arg1", type="var")
            else:
                content = ET.SubElement(el, "arg1", type=words[1].split("@")[0])
            content.text = words[1]

        case "CALL" | "LABEL" | "JUMP":
            if (len(words) != 2):
                print("Chybný počet argumentů")
                sys.exit(23)
            
            if (not regexLabelMatch(words[1])):
                print("Chybný formát argumentu")
                sys.exit(23)

            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            content = ET.SubElement(el, "arg1", type="label")
            content.text = words[1]

        case "ADD" | "SUB" | "MUL" | "IDIV" | "LT" | "GT" | "EQ" | "AND" | "OR" | "NOT" | "INT2CHAR" | "STRI2INT" | "CONCAT" | "GETCHAR" | "SETCHAR":
            if (len(words) != 4):
                print("Chybný počet argumentů")
                sys.exit(23)

            res, isVar = regexVarMatch(words[1])
            if (not res):
                print("Chybný formát argumentu")
                sys.exit(23)

            res2, isVar2 = regexVarMatch(words[2])
            if (not res2):
                print("Chybný formát argumentu")
                sys.exit(23)

            res3, isVar3 = regexVarMatch(words[3])
            if (not res3):
                print("Chybný formát argumentu")
                sys.exit(23)

            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            if (isVar):    
                content = ET.SubElement(el, "arg1", type="var")
            else:
                content = ET.SubElement(el, "arg1", type=words[1].split("@")[0])
            content.text = words[1]

            if (isVar2):    
                content = ET.SubElement(el, "arg2", type="var")
            else:
                content = ET.SubElement(el, "arg2", type=words[2].split("@")[0])
            content.text = words[2]

            if (isVar3):    
                content = ET.SubElement(el, "arg3", type="var")
            else:
                content = ET.SubElement(el, "arg3", type=words[3].split("@")[0])
            content.text = words[3]

        case "READ":
            if (len(words) != 3):
                print("Chybný počet argumentů")
                sys.exit(23)
            
            res, _ = regexVarMatch(words[1])
            if (not res):
                print("Chybný formát argumentu")
                sys.exit(23)
            
            if not re.match(r"(int|string|bool)$", words[2]):
                print("Chybný formát argumentu")
                sys.exit(23)

            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            content = ET.SubElement(el, "arg1", type="var")
            content.text = words[1]
            content = ET.SubElement(el, "arg2", type=words[2])
            content.text = words[2]

        case _:
            print("Neznámý opcode")
            sys.exit(22)
    
    orderInt = orderInt + 1

        
ET.indent(tree, space="    ")
tree.write("output.xml", encoding="UTF-8", xml_declaration=True)

