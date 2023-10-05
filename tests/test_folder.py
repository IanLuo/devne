from cli.folder import Folder, DATA_FOLDER

class TestFolder:
    def test_get_folder(self):
        name = "testUnit"
        assert Folder.get_data_path(name) == DATA_FOLDER + "/" + name
