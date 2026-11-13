import json, time, sys, urllib.parse, urllib.request, xml.etree.ElementTree as ET, os
sys.path.insert(0, os.path.dirname(__file__))
from conditions import *
BASE="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
RETMAX=int(os.environ.get("RETMAX","6"))
def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r: return r.read()
        except Exception as e:
            time.sleep(2*(i+1)); err=e
    raise err
def esearch(term, retmax=RETMAX, sort="relevance"):
    q=urllib.parse.urlencode({"db":"pubmed","term":term,"retmode":"json","retmax":retmax,"sort":sort})
    j=json.loads(get(BASE+"esearch.fcgi?"+q)); time.sleep(0.35)
    return int(j["esearchresult"]["count"]), j["esearchresult"]["idlist"]
def efetch(pmids):
    out={}
    for i in range(0,len(pmids),150):
        q=urllib.parse.urlencode({"db":"pubmed","id":",".join(pmids[i:i+150]),"retmode":"xml"})
        root=ET.fromstring(get(BASE+"efetch.fcgi?"+q)); time.sleep(0.35)
        for art in root.findall(".//PubmedArticle"):
            pmid=art.findtext(".//PMID")
            title="".join(art.find(".//ArticleTitle").itertext()) if art.find(".//ArticleTitle") is not None else ""
            abst=" ".join(("["+(a.get("Label") or "")+"] " if a.get("Label") else "")+"".join(a.itertext()) for a in art.findall(".//Abstract/AbstractText"))
            year=art.findtext(".//PubDate/Year") or (art.findtext(".//PubDate/MedlineDate") or "")[:4]
            doi=next((e.text for e in art.findall(".//ArticleId") if e.get("IdType")=="doi"),"")
            pts=[p.text for p in art.findall(".//PublicationType")]
            out[pmid]=dict(pmid=pmid,title=title,abstract=abst,year=year,doi=doi,journal=art.findtext(".//Journal/ISOAbbreviation") or "",pubtypes=pts)
    return out
if __name__=="__main__":
    log=[]; hits={}
    todo=[(k,v,QUERIES_BENEFIT) for k,v in BENEFIT.items()]+[(k,v,QUERIES_HARM) for k,v in HARM.items()]
    for key,(label,grp,term),Q in todo:
        total,_=esearch(term,0); log.append(dict(condition=key,evidence="TOTAL_LITERATURE",query=term,count=total))
        for ev,fn in Q.items():
            q=fn(term); n,ids=esearch(q)
            log.append(dict(condition=key,evidence=ev,query=q,count=n,retrieved=ids))
            for p in ids: hits.setdefault(p,[]).append([key,ev])
        print(key, file=sys.stderr)
    recs=efetch(list(hits))
    for p,r in recs.items(): r["hits"]=hits[p]
    json.dump(log,open("raw/search_log.json","w"),indent=1)
    json.dump(recs,open("raw/abstracts.json","w"),indent=1)
    print(len(log),"queries",len(recs),"abstracts")
