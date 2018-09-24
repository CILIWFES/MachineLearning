import os


class GlobalConstant:
    # 工程路径
    ROOT_PATH = os.path.abspath(os.path.join(os.getcwd(), "..")) + "\\"
    FILE_SUPPORT_PATH = ROOT_PATH + "FileSupport\\"

    CONFIG_FOLDER="\\Configuration\\"
    # 全局配置文件名
    GLO_CONFIG_FILENAME = "GlobalConfiguration.ini"
    # 全局配置文件路径
    GLO_CONFIG_PATH = FILE_SUPPORT_PATH + CONFIG_FOLDER + GLO_CONFIG_FILENAME

    # 文件夹路径
    SAVE_FOLDER_CONFIG = "Folder"
    SAVE_FILENAME_CONFIG = "FileName"

    # ORM框架配置文件section
    ORM_CONFIG_SECTION = "ORM"
