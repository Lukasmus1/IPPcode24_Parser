import sys
import xml.etree.ElementTree as ET


#Arg parser
args = sys.argv[1:]

if (len(args) == 1):
    if (args[0] == "--help"):
        print("Usage: python parse.py [options] [file]")
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