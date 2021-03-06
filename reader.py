import os
import pandas as pd
import glob


class ReadFile:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.all_documents = ''

    # def read_file(self):
    #     """
    #     This function is reading a parquet file contains several tweets
    #     The file location is given as a string as an input to this function.
    #     :param file_name: string - indicates the path to the file we wish to read.
    #     :return: a dataframe contains tweets.
    #     """
    #     # files = folders = 0
    #     # path = "E:\\Program Files\\לימודים\\שנה ד'\\אחזור\\Data\\Data"
    #     # for _, dirnames, filenames in os.walk(path):
    #     #     # ^ this idiom means "we won't be using this value"
    #     #     files += len(filenames)
    #     #     folders += len(dirnames)
    #
    #     # print
    #     # "{:,} files, {:,} folders".format(files, folders)
    #
    #
    #     files = glob.glob('./Data - Copy/**/*.parquet')
    #     df=pd.concat([pd.read_parquet(fp) for fp in files])
    #     # full_path = os.path.join(self.corpus_path, file_name)
    #     #
    #     # df = pd.read_parquet(full_path, engine="pyarrow")
    #     # list = df.values.tolist()
    #     return df.values.tolist()

    def read_file(self, file_name):
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        full_path = os.path.join(self.corpus_path, file_name)
        df = pd.read_parquet(full_path, engine="pyarrow")
        return df.values.tolist()

    def read_all_files(self):
        temp_folder_path = self.corpus_path
        for filename in os.listdir(self.corpus_path):
            if filename.endswith(".parquet"):
                self.all_documents.append(self.read_file(filename))
            elif os.path.isdir(self.corpus_path + '\\' + filename):
                for filenameParquet in os.listdir(self.corpus_path + '\\' + filename):
                    if filenameParquet.endswith(".parquet"):
                        temp_folder_path = self.corpus_path
                        self.corpus_path = self.corpus_path + '\\' + filename
                        self.all_documents = self.read_file(filenameParquet)
                        self.corpus_path = temp_folder_path
            else:
                continue
        return self.all_documents

    def get_all_path_of_parquet(self):
        pathes =[]
        for filename in os.listdir(self.corpus_path):
            if filename.endswith(".parquet"):
                pathes.append([self.corpus_path+"\\",filename])
            elif os.path.isdir(self.corpus_path + '\\' + filename):
                for filenameParquet in os.listdir(self.corpus_path + '\\' + filename):
                    if filenameParquet.endswith(".parquet"):
                        temp_folder_path = self.corpus_path
                        self.corpus_path = self.corpus_path + '\\' + filename
                        pathes.append([self.corpus_path ,filenameParquet])
                        self.corpus_path = temp_folder_path
            else:
                continue
        return pathes

    def get_documents(self,path,filename):
        full_path = os.path.join(path, filename)
        df = pd.read_parquet(full_path, engine="pyarrow")
        return df.values.tolist()