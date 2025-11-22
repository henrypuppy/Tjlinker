import json
from django.core.management.base import BaseCommand
from lists.models import Class

class Command(BaseCommand):
    help = 'Populate Class table with data from a JSON file'

    def handle(self, *args, **kwargs):
        # 读取文件内容
        file_path = 'Class.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()

        # 解析JSON数据
        options = json.loads(data)

        # 插入数据到数据库
        for option in options:
            first_value = option['value']
            for child in option['children']:
                second_value = child['value']
                Class.objects.create(First=first_value, Second=second_value)

        self.stdout.write(self.style.SUCCESS('数据插入完成'))