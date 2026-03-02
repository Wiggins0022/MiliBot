import os


def get_project_path() -> str:
    """
    获取项目根目录
    :return: 项目根目录
    """
    # 获取当前文件路径
    current_file_path = os.path.abspath(__file__)
    # 获取其所在文件夹
    current_dir = os.path.dirname(current_file_path)
    # 获取项目根目录
    project_path = os.path.dirname(current_dir)
    return project_path

def get_abs_path(relative_path: str) -> str:
    """
    获取相对于项目根目录的绝对路径
    :param relative_path: 相对路径
    :return: 绝对路径
    """
    project_path = get_project_path()
    abs_path = os.path.join(project_path, relative_path)
    return abs_path

if __name__ == '__main__':
    print("项目根目录:", get_project_path())
    print("绝对路径示例:", get_abs_path('agent/app.py'))