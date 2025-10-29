import argparse

parser = argparse.ArgumentParser(description="""
    This is a crutch script to retrieve identifiers 
    of genes that correspond to protein identifiers 
    and then get gene locations.
    """)

parser.add_argument('orgn', help='Organism name')
parser.add_argument('id', help='Genome assembly ID')

args = parser.parse_args()

data_path = f'../data/{args.orgn}/ncbi_dataset/data/{args.id}/genomic.gtf'
acc_path = f'../tree/{args.orgn}/acc_list.txt'

with open(acc_path) as file:
    acc_list = file.read().split()

prot_2_gene = {acc: '' for acc in acc_list}
exon_lists = {acc: [] for acc in acc_list}

with open(data_path) as file:
    for line in file:
        if not line.startswith('#'):
            line = line.split('\t')
            feature = line[2]
            info = line[-1]
            if feature == 'CDS':
                prot_id = info.split('protein_id "')[-1].split('"')[0]
                if prot_id in prot_2_gene.keys():
                    if not prot_2_gene[prot_id]:
                        gene = info.split('gene_id "')[-1].split('"')[0]
                        prot_2_gene[prot_id] = gene
                    exon = int(info.split('exon_number "')[-1].split('"')[0])
                    exon_lists[prot_id].append(exon)

gene_2_prots = {}
for prot, gene in prot_2_gene.items():
    if gene in gene_2_prots.keys():
        gene_2_prots[gene].append(prot)
    else:
        gene_2_prots[gene] = [prot]

canonical = {gene: ['', ''] for gene in gene_2_prots.keys()}

seq_path = f'../tree/{args.orgn}/blastp_res_filtered.faa'
with open(seq_path) as file:
    seq = ''
    seq_id = ''
    for line in file:
        if line.startswith('>'):
            if seq_id:
                gene = prot_2_gene[seq_id]
                if gene not in canonical.keys():
                    canonical[gene] = [seq_descr, seq]
                elif len(seq) > len(canonical[gene][0]):
                    canonical[gene] = [seq_descr, seq]
            seq_id = line[1:].split()[0]
            seq_descr = line.rstrip()
            seq = ''
        else:
            seq += line.rstrip()

gene = prot_2_gene[seq_id]
if gene not in canonical.keys():
    canonical[gene] = [seq_descr, seq]
elif len(seq) > len(canonical[gene][0]):
    canonical[gene] = [seq_descr, seq]

with open(f'../tree/{args.orgn}/canonical_sequences.faa', 'w') as outfile:
    for descr, seq in canonical.values():
        print(descr, file=outfile)
        print(seq, file=outfile)

print('Gene ID'.ljust(15), 'Protein ID'.ljust(15), 'Exons')

for gene, prots in gene_2_prots.items():
    print(gene.ljust(15), prots[0].ljust(15), exon_lists[prots[0]])
    for prot in prots[1:]:
        print(' '* 15, prot.ljust(15), exon_lists[prot])