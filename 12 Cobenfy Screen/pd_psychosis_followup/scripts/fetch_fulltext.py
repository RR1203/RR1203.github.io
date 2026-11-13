import json,urllib.request,urllib.parse,re,time,sys
P=sys.argv[1].split(',')
def get(u):
    for i in range(5):
        try:
            with urllib.request.urlopen(u,timeout=60) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(3*(i+1)); continue
            raise
    raise RuntimeError('429')
j=json.loads(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id="+",".join(P)))
try: meta=json.load(open('raw/pdp_meta.json'))
except: meta={}
for p in P:
    d=j['result'][p]; ids={a['idtype']:a['value'] for a in d['articleids']}
    m=dict(title=d['title'],journal=d['fulljournalname'],date=d['pubdate'],pmc=ids.get('pmc',''),doi=ids.get('doi',''))
    txt=''
    if m['pmc']:
        try:
            x=get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{m['pmc']}/fullTextXML").decode()
            txt=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',x))
        except Exception as e: m['ft_err']=str(e)
    m['fulltext']=bool(txt); open(f'raw/fulltext_{p}.txt','w').write(txt); meta[p]=m
    print(p,m['pmc'] or '-',len(txt),'|',m['title'][:70]); time.sleep(0.5)
json.dump(meta,open('raw/pdp_meta.json','w'),indent=1)
