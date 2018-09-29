import os


class GlobalConstant:
    # 工程路径,三级目录
    ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "\\"
    SUPPORT_PATH = ROOT_PATH + "FileSupport\\"

    CONFIG_FOLDER = "\\Configuration\\"
    # 全局配置文件名
    GLO_CONFIG_FILENAME = "GlobalConfiguration.ini"
    # 全局配置文件路径
    GLO_CONFIG_PATH = SUPPORT_PATH + CONFIG_FOLDER + GLO_CONFIG_FILENAME

    """
    配置文件中名字的统一命名
    Section:大类
    Name:大类下的项
    """
    # 文件夹路径
    SAVE_FOLDER_CONFIG = "Folder"
    SAVE_FILENAME_CONFIG = "FileName"
    SAVE_BUNCHNAME_CONFIG = "BunchName"

    """
    Section:大类
    """
    # ORM框架配置文件section
    ORM_CONFIG_SECTION = "ORM"
    STOPWORDS_CONFIG_SECTION = "StopWords"

    """
    Segmentation大类(分隔符)
    """
    Segmentation_CONFIG_SECTION = "Segmentation"
    Jieba_Segmentation="jieba"


