import csv, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for f in 'author1 author2 author3 author4 author5 author6 author7 author8'.split(): exec(open(f+'.py').read())
def w(path, header, rows):
    with open(path,'w',encoding='utf-8',newline='') as fh:
        fh.write('\t'.join(header)+'\n')
        for r in rows:
            for x in r: assert '\t' not in x and '\n' not in x, r[0]
            fh.write('\t'.join(r)+'\n')
os.makedirs('scenes',exist_ok=True)
w('scenes/all.clusters.tsv',['cluster','frame','sentence_nl','sentence_en'],CL)
w('scenes/all.cards.tsv',['id','scene','must','avoid','contrast','split','example_nl','example_en','perfect','alt'],CD)
print(len(CL),len(CD))
