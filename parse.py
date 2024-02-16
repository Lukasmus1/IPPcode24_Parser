import sys
import os
import re
import xml.etree.ElementTree as ET

def regexVarMatch(string):
    if (string.count("@") < 1):
        print("Chybný formát argumentu")
        sys.exit(23)
    words = string.split("@", 1)
    var = re.match(r"^(GF|LF|TF)", words[0]) is not None
    var = var and regexLabelMatch(words[1])
    return var
      

def regexSymMatch(string):
    if (string.count("@") < 1):
        print("Chybný formát argumentu")
        sys.exit(23)
    arg = string.split("@", 1)

    match arg[0]:
        case "int":
            res = re.match(r"^[-+]?[0-9]+$", arg[1]) is not None
            res = res or (re.match(r"^-(0x)?[0-9a-fA-F]+$|^(0x)?[0-9a-fA-F]+$", arg[1]) is not None)
            res = res or (re.match(r"^-(0o)?[0-7]+$|^(0o)?[0-7]+$", arg[1]) is not None)
            res = res or (re.match(r"^(0b)?[01]+$", arg[1]) is not None)
            return res
        case "bool":
            return re.match(r"^(true|false)$", arg[1]) is not None
        case "string":
            return re.match(r"^([^\s#\\]|\\[0-9]{3})*(?<!\\)$", arg[1]) is not None
        case "nil":
            return re.match(r"^nil$", arg[1]) is not None
        case _:
            return False

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
root = ET.Element("program")
root.set("language", "IPPcode24")

# Vytvoření stromu z kořenového elementu
tree = ET.ElementTree(root)


#Kontrola hlavičky
helper = False
for line in sys.stdin:
    ind = line.find("#")
    if (ind != -1):
        line = line[:ind]

    line = line.strip()
    if(len(line) == 0):
        continue

    if (line.lower() == ".ippcode24"):
        helper = True
        break
    else:
        print("Chybná hlavička")
        sys.exit(21)

if (not helper):
    print("Chybí hlavička")
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

            res = regexVarMatch(words[1])

            if (not res):
                print("Chybný formát argumentu")
                sys.exit(23)

            res = regexVarMatch(words[2])
            isVar = regexSymMatch(words[2])
            if (not (res or isVar)):
                print("Chybný formát argumentu")
                sys.exit(23)

            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            content = ET.SubElement(el, "arg1", type="var")
            content.text = words[1]

            if (not isVar):
                content = ET.SubElement(el, "arg2", type="var")
                content.text = words[2]
            else:
                wordsSplit = words[2].split("@", 1)
                content = ET.SubElement(el, "arg2", type=wordsSplit[0])
                content.text = wordsSplit[1]

        case "CREATEFRAME" | "PUSHFRAME" | "POPFRAME" | "RETURN" | "BREAK":
            if (len(words) != 1):
                print("Chybný počet argumentů")
                sys.exit(23)
            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)


        case "DEFVAR" | "POPS":
            if (len(words) != 2):
                print("Chybný počet argumentů")
                sys.exit(23)

            res = regexVarMatch(words[1])

            if (not res):
                print("Chybný formát argumentu")
                sys.exit(23)
            
            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            content = ET.SubElement(el, "arg1", type="var")
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

        case "ADD" | "SUB" | "MUL" | "IDIV" | "LT" | "GT" | "EQ" | "AND" | "OR" | "INT2CHAR" | "STRI2INT" | "CONCAT" | "GETCHAR" | "SETCHAR":
            if (len(words) != 4):
                print("Chybný počet argumentů")
                sys.exit(23)

            res = regexVarMatch(words[1])
            if (not res):
                print("Chybný formát argumentu")
                sys.exit(23)

            res = regexVarMatch(words[2])
            isVar = regexSymMatch(words[2])
            if (not (res or isVar)):
                print("Chybný formát argumentu")
                sys.exit(23)

            res2 = regexVarMatch(words[3])
            isVar2 = regexSymMatch(words[3])
            if (not (res2 or isVar2)):
                print("Chybný formát argumentu")
                sys.exit(23)

            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            content = ET.SubElement(el, "arg1", type="var")
            content.text = words[1]

            if (not isVar):    
                content = ET.SubElement(el, "arg2", type="var")
                content.text = words[2]
            else:
                wordsSplit = words[2].split("@", 1)
                content = ET.SubElement(el, "arg2", type=wordsSplit[0])
                content.text = wordsSplit[1]

            if (not isVar2):    
                content = ET.SubElement(el, "arg3", type="var")
                content.text = words[3]
            else:
                wordsSplit = words[3].split("@", 1)
                content = ET.SubElement(el, "arg3", type=wordsSplit[0])
                content.text = wordsSplit[1]

        case "NOT":
            if (len(words) != 3):
                print("Chybný počet argumentů")
                sys.exit(23)

            res = regexVarMatch(words[1])
            if (not res):
                print("Chybný formát argumentu")
                sys.exit(23)

            res = regexVarMatch(words[2])
            isVar = regexSymMatch(words[2])
            if (not (res or isVar)):
                print("Chybný formát argumentu")
                sys.exit(23)

            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            content = ET.SubElement(el, "arg1", type="var")
            content.text = words[1]

            if (not isVar):    
                content = ET.SubElement(el, "arg2", type="var")
                content.text = words[2]
            else:
                wordsSplit = words[2].split("@", 1)
                content = ET.SubElement(el, "arg2", type=wordsSplit[0])
                content.text = wordsSplit[1]


        case "READ":
            if (len(words) != 3):
                print("Chybný počet argumentů")
                sys.exit(23)
            
            res = regexVarMatch(words[1])
            if (not res):
                print("Chybný formát argumentu")
                sys.exit(23)
            
            if not re.match(r"(int|string|bool)$", words[2]):
                print("Chybný formát argumentu")
                sys.exit(23)

            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            content = ET.SubElement(el, "arg1", type="var")
            content.text = words[1]
            content = ET.SubElement(el, "arg2", type="type")
            content.text = words[2]

        case "JUMPIFEQ" | "JUMPIFNEQ":
            if (len(words) != 4):
                print("Chybný počet argumentů")
                sys.exit(23)
            
            if (not regexLabelMatch(words[1])):
                print("Chybný formát argumentu")
                sys.exit(23)
            
            res = regexVarMatch(words[2])
            isVar = regexSymMatch(words[2])
            if (not (res or isVar)):
                print("Chybný formát argumentu")
                sys.exit(23)
            
            res2 = regexVarMatch(words[3])
            isVar2 = regexSymMatch(words[3])
            if (not (res2 or isVar2)):
                print("Chybný formát argumentu")
                sys.exit(23)
            
            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            content = ET.SubElement(el, "arg1", type="label")
            content.text = words[1]

            if (not isVar):
                content = ET.SubElement(el, "arg2", type="var")
                content.text = words[2]
            else:
                wordsSplit = words[2].split("@", 1)
                content = ET.SubElement(el, "arg2", type=wordsSplit[0])
                content.text = wordsSplit[1]

            if (not isVar2):
                content = ET.SubElement(el, "arg3", type="var")
                content.text = words[3]
            else:
                wordsSplit = words[3].split("@", 1)
                content = ET.SubElement(el, "arg3", type=wordsSplit[0])
                content.text = wordsSplit[1]

        case "EXIT" | "DPRINT" | "WRITE" | "PUSHS":
            if (len(words) != 2):
                print("Chybný počet argumentů")
                sys.exit(23)

            res = regexVarMatch(words[1])
            isVar = regexSymMatch(words[1])
            
            if (not (res or isVar)):
                print("Chybný formát argumentu")
                sys.exit(23)
            
            el = ET.SubElement(root, "instruction", order=str(orderInt), opcode=opcode)
            if (not isVar):
                content = ET.SubElement(el, "arg1", type="var")
                content.text = words[1]
            else:
                wordsSplit = words[1].split("@", 1)
                content = ET.SubElement(el, "arg1", type=wordsSplit[0])
                content.text = wordsSplit[1]


        case _:
            print("Neznámý opcode")
            sys.exit(22)
    
    orderInt = orderInt + 1

        
ET.indent(tree, space="    ")

xml_string = ET.tostring(root, encoding='utf-8', method="xml")
xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_string.decode('utf-8')

print(xml_string)
