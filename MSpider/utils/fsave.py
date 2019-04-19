import json


class ItemFile(object):
    def save_to_json(self, filename, source_data):
        '''
        把解析器解析后的数据存成json格式
        :param filename: 文件名
        :param source_data: 元数据
        :return:
        '''
        raise NotImplementedError

    def dumps_json(self, data):
        '''
        把data转换为json对象
        :param data: 元数据
        :return:
        '''
        return json.dumps(data, ensure_ascii=False)

    def loads_json(self, data):
        '''
        把data转换为python数据类型
        :param data: 元数据
        :return:
        '''
        return json.loads(data, encoding='utf-8')

    def save_excel(self, filename, source_data):
        '''
        保存为excel格式
        :param filename: 文件名
        :param source_data: 元数据
        :return:
        '''
        raise NotImplementedError

