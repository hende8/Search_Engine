import os
import pandas as pd


class ReadFile:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    def read_file(self, file_name):
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        full_path = os.path.join(self.corpus_path, file_name)
        df = pd.read_parquet(full_path, engine="pyarrow")
        print(df)
        return df.values.tolist()

    def read_all_files(self):
        for filename in os.listdir(self.corpus_path):
            folder = self.corpus_path +'\\'+filename
            if os.path.isdir(self.corpus_path +'\\'+filename):
                for filenameParquet in os.listdir(folder):
                    if  filenameParquet.endswith(".parquet"):
                        folder=folder+'\\'+filenameParquet
                        self.read_file(folder)
                        break
            else:
                continue