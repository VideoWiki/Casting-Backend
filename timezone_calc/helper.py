def get_latest_logs(path, number_of_logs=500):
    """
    get latest numbers of logs from log file
    :param path: path of log file
    :param number_of_logs: number of logs to fetch
    :return: String
    """
    with open(path) as f:
        text = f.readlines()[-number_of_logs:]
        text.reverse()
    return "\n".join(text)