from os.path import dirname, exists
from folder import Folder
from user_interactive.user_input_wizard import UserInputWizard, InputItem
from resources.remote.global_configure import GlobalConfigure

def init_default_config(config_path: str):
    folder = Folder(dirname(config_path))

    if not exists(folder.config_path):
        config_wizard = UserInputWizard([
            InputItem(False, 'name'),
            InputItem(False, 'version'),
            InputItem(False, 'language'),
            InputItem(False, 'version of language' ),
            InputItem(False, 'description'),
        ])

        config = config_wizard.run()
        name = config['name']
        version = config['version']
        language = config['language']
        version_of_language = config['version of language']
        description = config['description']
        nixpkgs_rev = GlobalConfigure.fetch_nixpkgs_rev()

        current_directory = dirname(__file__)
        path = f'{current_directory}/ss.yaml.template'
        with open(path, 'r') as f:
            content = f.read()
            content = content.replace('#NAME#', name)
            content = content.replace('#DESCRIPTION#', description)
            content = content.replace('#VERSION#', version)
            content = content.replace('#SDK_LANGUAGE#', language)
            content = content.replace('#SDK_VERSION#', version_of_language)
            content = content.replace('#NIXPKGSREV#', nixpkgs_rev)

            folder.make_file(folder.config_path, content)
    else:
        raise Exception('config file already exists')
