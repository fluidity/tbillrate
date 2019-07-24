###############################################
# NOTE: DO NOT USE THIS, SEE testparselxml.py #
###############################################


import xml.etree.ElementTree as ET


def parseXML(xmlfile):
    namespaces = {"atom": "http://www.w3.org/2005/Atom"}

    # Parse the file
    tree = ET.parse(xmlfile)
    # Get the main element
    root = tree.getroot()
    print("Root:")
    print(root)

    print("\nIn root:")
    for item in root:
        print(item)

    print("\nEntries:")
    for item in root.findall('atom:entry', namespaces):
        print(item)

    print("\nEnd")

rates = parseXML("DailyTreasuryBillRateData.xml")

