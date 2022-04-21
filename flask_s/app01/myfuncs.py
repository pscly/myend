

def write_data(data):
    """
    写数据
    :return:
    """
    write_file(data)


def write_file(data: dict):
    """
    写文件
    :param data:
    :param file_name:
    :return:
    """
    with open(f"data/y_data_{data.get('who')}.txt", 'a', encoding='utf-8') as f:
        for i in data:
            f.write(f'{str(data[i])},')
        f.write('\n')


def save_file(file, file_path):
    """
    保存文件
    """

    with open(file_path, 'wb') as f:
        f.write(file.read())
