search_text_start = '[CorrelationFunction]\n'
search_text_end = '\n[RawCorrelationFunction]'


def read_correlator_text_file():
    with open('data\\test.sin', 'r') as file:
        return file.read()


def write_modified_correlator_text_file(text):
    with open('data\\output.txt', 'w') as file:
        file.write(text)


def trim_correlator_text_file(text):
    idx_start = (text.find(search_text_start)) + len(search_text_start)
    idx_end = (text.find(search_text_end))
    return text[idx_start:idx_end]


if __name__ == '__main__':
    file_text = read_correlator_text_file()
    new_text = trim_correlator_text_file(file_text)
    write_modified_correlator_text_file(new_text)

