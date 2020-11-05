import search_engine
import reader
if __name__ == '__main__':
    rd = reader.ReadFile(corpus_path= 'C:\\Users\\HEN\\PycharmProjects\\Search_Engine_Project\\Data')
    # rd = reader.ReadFile()
    # rd.read_file("covid19_07-08.snappy.parquet")
    rd.read_all_files()
    search_engine.main()
