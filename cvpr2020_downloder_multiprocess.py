# @modified:  cyliu7
# @date:      2020.06.12

import requests
from bs4 import BeautifulSoup
import os
import numpy as np
from multiprocessing import Process 

import sys
sys.setrecursionlimit(100000) 

headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }
url="http://openaccess.thecvf.com/CVPR2020.py"
html=requests.get(url)

soup=BeautifulSoup(html.content)

soup.a.contents=='pdf'

pdfs=soup.findAll(name="a",text="pdf")

if not os.path.exists('./CVPR2020_/'):
        os.mkdir('./CVPR2020_/') 
folder_path='./CVPR2020_/'

def download_func(begin, end):
    pdf_lists = pdfs[begin:end]
    for i, pdf in enumerate(pdf_lists):
        pdf_name=pdf["href"].split('/')[-1]
        c=requests.get('http://openaccess.thecvf.com/'+pdf['href'],headers=headers).content
        with open(folder_path+pdf_name,mode="wb") as f:
                f.write(c)
                print('['+str(i)+']'+pdf_name+" finish")

if __name__ == "__main__":



        CPUS = 4
        sep_list_id = list(np.linspace(0, len(pdfs), CPUS + 1, dtype = np.int))
        # print(sep_list_id)

        recors_process = list()

        for cpu_i in range(CPUS):
                p = Process(target = download_func, args = (sep_list_id[cpu_i], sep_list_id[cpu_i + 1], ) )
                p.start()
                recors_process.append(p)

        for p in recors_process:
                p.join()
