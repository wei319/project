# this file is to open the csv file to fetch the weblink of the cDNA clones
# and then use the cDNA clone info to make our vector sequence info

import requests
import pandas as pd
from bs4 import BeautifulSoup

#   first pre-define some vector information and print the html head part
head_html = '''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Gene info and vector sequences</title>
</head>
'''

end_html = '''<body>
</body>
</html>
'''

cDNA_start = '''<span style='font-family:"Segoe UI",sans-serif'><span style='color:#F40000'><em>Red</span>=Cloning site
<span style='color:#0000cc'>Blue</span>=ORF <span style='color:#50882b'>Green</span>=Tags(s)<br></em>
TTTTGTAATACGACTCACTATAGGGCGGCCGGGAATTCGTCGACT<u>GGATCCGGTACCGAGGAGATCTGC</u>CGCC<span style='color:#F40000'>GCGATCGC</span><span style='color:#50882b'>C</span><br>
'''

cDNA_end = '''
<u><span style='color:#F40000'>ACGCGT</span><span style='color:#50882b'>ACGCGGCCGCTCGAG</u>CAGAAACTCATCTCAGAAGAGGATCTGGCAGCAAATGATATCCTGGATT<br>ACAAGGATGACGACGATAAG</span>GTTTAA</div></span></p>
'''

pBabe_start = '''<p><div id="pBabe vector">
<em><span style='color:#666666;background:aqua;mso-highlight:aqua;mso-shading:white'>BamHI</span>&nbsp;&nbsp;&nbsp;<span style='background:fuchsia;
mso-highlight:fuchsia'>XhoI</span>&nbsp;&nbsp;&nbsp;<span style='color:black;mso-color-alt:windowtext;background:#FABF8F;mso-shading-themecolor:
accent6;mso-shading-themetint:153'>3XFLAG tag</span>&nbsp;&nbsp;&nbsp;<span style='background:lime;mso-highlight:lime'>EcoRI</span><br></em>
<span style='font-family:"Courier New"'>
<u>CTTTATCCAGCCCTCAC</u>TCCTTCTCTAGGCGCCGGCC<br>
<u><span style='color:#666666;background:aqua;mso-highlight:aqua;mso-shading:white'>GGATCC</span>GGTACCGAGGAGATCTGC</u>CGCC<span style='color:#F40000'>GCGATCGC</span>C<br>
'''

pBabe_end = '''
<u><span style='color:#F40000'>ACGCGT</span><span style='color:#50882B'>ACGCGGCCG</span><span style='background:fuchsia;
mso-highlight:fuchsia'>CTCGAG</span></u><br>
GGCCGC<span style='color:black;mso-color-alt:windowtext;background:#FABF8F;mso-shading-themecolor:
accent6;mso-shading-themetint:153'>GACTACAAGGATGACGATGACAAGGATTACAAAGACGACGATGATAAGGACTATAAGGATGATGACGACAAA</span>TAATAG<span style='background:lime;mso-highlight:lime'>GAATTC</span>GCCAGCACAGTGGTCGAC</div></span></p>
'''


with open("gene_vector_info.html", 'w') as html_file:
    html_file.write(head_html)


#   second read the csv file to get the gene information and cDNA vector url
gene_file = pd.read_csv("source_data/gene_info_data.csv")

# print(gene_file)

"""
        sku   Well  ...  availability                                                url
0  MR200116  1-A-1  ...      In Stock  https://www.origene.com/catalog/cdna-clones/ex...
1  MR200721  1-A-2  ...      In Stock  https://www.origene.com/catalog/cdna-clones/ex...
2  MR200827  1-A-3  ...      In Stock  https://www.origene.com/catalog/cdna-clones/ex...
3  MR201061  1-A-4  ...      In Stock  https://www.origene.com/catalog/cdna-clones/ex...
4  MR201177  1-A-5  ...      In Stock  https://www.origene.com/catalog/cdna-clones/ex...
5  MR201714  1-A-6  ...      In Stock  https://www.origene.com/catalog/cdna-clones/ex...

[6 rows x 12 columns]
"""
'''sku	Well	symbol	Length(ORF length)
MR200116	1-A-1	Apln	234
MR200721	1-A-2	Tnfrsf12a	390
MR200827	1-A-3	Calca	411
MR201061	1-A-4	Thrsp	453
MR201177	1-A-5	Mafk	471
MR201714	1-A-6	Tmem140	558
'''
# print(gene_file.Well)
for ind in gene_file.index:

    #   construct the gene information and vector name
    cDNA_name = gene_file['Well'][ind].replace("-", "") + "-" + gene_file['symbol'][ind] + "-3XFLAG"    #1A1-Apln-3XFLAG
    #   construct the newly cloned pBabe vector name as pBabe name
    pBabe_name = gene_file['symbol'][ind] + "-3XFLAG vector"
    # print(cDNA_name)

    #   read the url and get useful vector information
    res = requests.get(gene_file.url[ind]).text
    content = BeautifulSoup(res, "html.parser")
    cDNA_vec_name = content.find('div', attrs={'id': 'sequence'})
    # print(cDNA_vec_name.text.splitlines()[0])
    if cDNA_vec_name is None:
        continue

    data = content.find_all('span', attrs={'class': 'origene-sequence-blue'})
    gene_seq = "<br>".join(data[1].text.splitlines())
    #   print(gene_seq)

    #   write the information in to html file
    with open("gene_vector_info.html", 'a') as html_file:
        html_file.write(f"<h1>{cDNA_name}&nbsp;-&nbsp;{gene_file['Length'][ind]}&nbsp;bp</h1>")
        html_file.write(f"<h2>{gene_file['Well'][ind]} Origene clone</h2>")
        html_file.write(f'<p><div id="Origene clone">{cDNA_vec_name.text.splitlines()[0]}<br>')

        html_file.write(cDNA_start)
        html_file.write(f"<span style = 'color:#0000cc'>{gene_seq}</span><br>")
        html_file.write(cDNA_end)

        html_file.write(f"<h2>{pBabe_name}</h2>")
        html_file.write(pBabe_start)
        html_file.write(f"<span style='color:#0000cc'>{gene_seq}</span><br>")
        html_file.write(pBabe_end)


with open("gene_vector_info.html", 'a') as html_file:
    html_file.write(end_html)
    html_file.close()
