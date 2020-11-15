"""
页面缓存
"""
import hashlib
import json
import os

from django.http import JsonResponse

from ct_tools.django_utils.requests import find_request


class PageCache:
    def __init__(self, path: str):
        if os.path.isdir(path):
            self.path = path
        else:
            raise Exception("path 参数必须是存在的目录")

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            request = find_request(*args, **kwargs)
            path_ = request.path.encode("utf-8")
            body_ = request.body
            university_ = request.user.university.encode("utf-8")
            md_ = hashlib.md5(path_ + body_ + university_)
            filename = md_.hexdigest()
            store_path = os.path.join(self.path, "static", "cache")
            if not os.path.exists(store_path):
                os.mkdir(store_path)
            fname_list = os.listdir(store_path)
            real_filename = os.path.join(store_path, filename)
            if filename in fname_list:
                content = json.load(open(real_filename))
                return JsonResponse(content)
            else:
                resp = func(*args, **kwargs)
                json.dump(resp.content.decode(), open(real_filename, "w"))
                return resp

        return wrapper