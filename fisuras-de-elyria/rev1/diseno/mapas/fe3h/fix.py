import sys
from collections import Counter
def fill(g,cells):
    S=set(cells)
    for _ in range(4):
        for (c,r) in list(S):
            cnt=Counter()
            for dr,dc in((1,0),(-1,0),(0,1),(0,-1)):
                rr,cc=r+dr,c+dc
                if 0<=rr<len(g) and 0<=cc<len(g[0]) and (cc,rr) not in S and g[rr][cc] in '.FR': cnt[g[rr][cc]]+=1
            if not cnt: cnt[ '.' ]=1
            if cnt:
                best=max(cnt.items(),key=lambda kv:(kv[1],kv[0]=='.'))[0]
                g[r][c]=best; S.discard((c,r))
    return g
def save(name,hdr,g):
    open(name,'w').write(hdr+"\n"+"\n".join("".join(r) for r in g)+"\n")
    print("\n".join("".join(r) for r in g))
