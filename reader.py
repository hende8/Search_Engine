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
        # files = folders = 0
        # path = "E:\\Program Files\\לימודים\\שנה ד'\\אחזור\\Data\\Data"
        # for _, dirnames, filenames in os.walk(path):
        #     # ^ this idiom means "we won't be using this value"
        #     files += len(filenames)
        #     folders += len(dirnames)
        #
        # print
        # "{:,} files, {:,} folders".format(files, folders)



        full_path = os.path.join(self.corpus_path, file_name)

        df = pd.read_parquet(full_path, engine="pyarrow")
        return df.values.tolist()
