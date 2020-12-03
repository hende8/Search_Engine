class ConfigClass:
    def __init__(self,corpuspath,outputpath,stemming):
        self.corpusPath =corpuspath
        #### outputpath
        self.savedFileMainFolder = outputpath

        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        #stemmming
        self.toStem = stemming

        print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath
