import spacy
import pandas as pd
from NER2 import *
from pandas.core.frame import DataFrame
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support


def process_chunk(chunk):
    datalist = chunk.iloc[:, 1].astype(str).tolist()
    filelist = chunk.iloc[:, 0].astype(str).tolist()

    docs = GeoEntityRecognize2(datalist)

    filelist_result = []
    attrlist = []
    labellist = []
    entitylist = []
    sentencelist = []
    empty_df = pd.DataFrame()
    for idx, doc in enumerate(docs):
        filename = filelist[idx]

        #geological_relations =extract_geological_facies_fm_in_sentence(doc,50,filename=filelist[idx])
        geological_relations=extract_geological_proxcy_x_in_sentence2(doc,"STROMA",50,filename=filelist[idx])

        empty_df = pd.concat([empty_df, geological_relations], ignore_index=True)

    return empty_df


if __name__ == '__main__':
    freeze_support()

    chunk_size =4
  
    file_path=r""

    chunks = []
    start_idx=1

    # Load chunks into memory
    for chunk in pd.read_csv(file_path,   chunksize=chunk_size):
        chunks.append(chunk)


    with ProcessPoolExecutor(max_workers=40) as executor:
        for idx, result in enumerate(executor.map(process_chunk, chunks[start_idx:])):

            df3 = pd.DataFrame(result)


            if df3.empty:
                 continue
            
            df3.to_csv(f"E:\\temp\\stroma_chunk_{idx + start_idx}.csv", mode='a',header=False)