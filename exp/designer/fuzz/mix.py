import glob,collections,re
c=collections.Counter(); feats=collections.Counter(); n=0; acc=[]
for r in glob.glob('work/*.res'):
    seed=r.split('/s')[-1].split('.')[0]
    res=open(r).read().split()
    mode=open(f'work/s{seed}.feat').read().split('\n')[0]
    c[(mode,res[2])]+=1
    if mode=='ok' and res[2]!='ok': acc.append(seed)
    for f in open(f'work/s{seed}.feat').read().split('\n')[1:]:
        if f: feats[f]+=1
    n+=1
print(n,sorted(c.items()))
print('accidental non-ok:',acc[:20])
print(sorted(feats.items(), key=lambda x:x[0]))
