"""Convert each DailyMed SPL XML version to plain text, section by section. Usage: python -I 03_label_text.py <spl.xml> <out.txt>"""
import sys, xml.etree.ElementTree as ET
NS = {'v': 'urn:hl7-org:v3'}
t = ET.parse(sys.argv[1]); r = t.getroot()
out = []
eff = r.find('v:effectiveTime', NS); ver = r.find('v:versionNumber', NS)
out.append(f"EFFECTIVE {eff.get('value') if eff is not None else ''} VERSION {ver.get('value') if ver is not None else ''}")
def walk(sec, depth):
    title = sec.find('v:title', NS)
    out.append('\n' + '#' * depth + ' ' + (' '.join(''.join(title.itertext()).split()) if title is not None else ''))
    text = sec.find('v:text', NS)
    if text is not None:
        for el in text.iter():
            tag = el.tag.split('}')[1]
            if tag == 'paragraph' or tag == 'item' or tag == 'caption':
                s = ' '.join(''.join(el.itertext()).split())
                if s: out.append(s)
            if tag == 'tr':
                out.append(' | '.join(' '.join(''.join(c.itertext()).split()) for c in el if c.tag.split('}')[1] in ('td', 'th')))
    for comp in sec.findall('v:component/v:section', NS): walk(comp, depth + 1)
for sec in r.findall('.//v:structuredBody/v:component/v:section', NS): walk(sec, 1)
open(sys.argv[2], 'w').write('\n'.join(out))
