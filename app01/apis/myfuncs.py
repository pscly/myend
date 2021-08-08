

def write_data(data):
    """
    写数据
    :return:
    """
    write_file(data)

def write_file(data):
    """
    写文件
    :param data:
    :param file_name:
    :return:
    """
    with open(f"data/{data['who']}.txt", 'a') as f:
        for i in data:
            f.write(data[i] + ',')
        f.write('\n')
