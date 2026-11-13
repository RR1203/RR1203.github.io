"""Dump every table in a JATS full-text XML (Europe PMC) as plain text rows. Usage: python -I 02_xml_tables.py file.xml"""
import sys, xml.etree.ElementTree as ET
t = ET.parse(sys.argv[1])
def txt(e): return ' '.join(''.join(e.itertext()).split())
for tw in t.iter('table-wrap'):
    lab = tw.find('label'); cap = tw.find('caption')
    print('#####', txt(lab) if lab is not None else '', '|', txt(cap) if cap is not None else '')
    for tr in tw.iter('tr'):
        print(' | '.join(txt(c) for c in tr if c.tag in ('td', 'th')))
    for fn in tw.iter('table-wrap-foot'): print('FOOT:', txt(fn))
