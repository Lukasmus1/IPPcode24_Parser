import sys
import os
import xml.etree.ElementTree as ET


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

# Vytvoření stromu z kořenového elementu
tree = ET.ElementTree(root)

# Uložení stromu do souboru s definovaným kódováním
tree.write("output.xml", encoding="UTF-8", xml_declaration=True)


#Kontrola hlavičky
if (sys.stdin.readline().strip() != ".IPPcode24"):
    print("Chybná hlavička")
    sys.exit(21)


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
    match words[0].upper():
        case "MOVE":
            print("MOVE")
        case "CREATEFRAME":
            print("CREATEFRAME")
        case "PUSHFRAME":
            print("PUSHFRAME")
        case "POPFRAME":
            print("POPFRAME")
        case "DEFVAR":
            print("DEFVAR")
        case "CALL":
            print("CALL")
        case "RETURN":
            print("RETURN")
        case "PUSHS":
            print("PUSHS")
        case "POPS":
            print("POPS")
        case "ADD":
            print("ADD")
        case "SUB":
            print("SUB")
        case "MUL":
            print("MUL")
        case "IDIV":
            print("IDIV")
        
    