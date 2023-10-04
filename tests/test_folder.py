from cli.folder import Folder, DATA_FOLDER

class TestFolder:
    def testGetFolder(self):
        name = "testUnit"
        assert Folder.getDataPath(name) == DATA_FOLDER + "/" + name
