from datetime import datetime
import requests


def find_max_dpi(dict_in_search):
    max_dpi = 0
    need_elem = 0
    for j in range(len(dict_in_search)):
        file_dpi = dict_in_search[j].get('width') * dict_in_search[j].get('height')
        if file_dpi > max_dpi:
            max_dpi = file_dpi
            need_elem = j
    return dict_in_search[need_elem].get('url'), dict_in_search[need_elem].get('type')


def time_convert(time_unix):
    time_bc = datetime.fromtimestamp(time_unix)
    str_time = time_bc.strftime('%Y-%m-%d time %H-%M-%S')
    return str_time


class VkRequest:
    def __init__(self, token, user_id, version='5.131'):
        self.token = token
        self.id = user_id
        self.version = version
        self.start_params = {'access_token': self.token, 'v': self.version}
        self.json, self.export_dict = self._sort_info()

    def _get_photo_info(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'album_id': 'profile',
            'photo_size': 1,
            'extended': 1,
            'rev': 1
        }
        response = requests.get(url, params={**self.start_params, **params})
        if response.status_code != 200:
            raise RuntimeError('Не авторизирован в сервисе вк')
        photo_info: dict = response.json()['response']
        return photo_info['count'], photo_info['items']

    def _get_logs_only(self):
        photo_count, photo_items = self._get_photo_info()
        result = {}
        for i in range(photo_count):
            likes_count = photo_items[i]['likes']['count']
            url_download, picture_size = find_max_dpi(photo_items[i]['sizes'])
            time_wrap = time_convert(photo_items[i]['date'])
            new_value = result.get(likes_count, [])
            new_value.append({'likes_count': likes_count,
                              'add_name': time_wrap,
                              'url_picture': url_download,
                              'size': picture_size
                              })
            result[likes_count] = new_value
        return result

    def _sort_info(self):
        json_list = []
        sorted_dict = {}
        picture_dict = self._get_logs_only()
        for elem in picture_dict.keys():
            for value in picture_dict[elem]:
                if len(picture_dict[elem]) == 1:
                    file_name = f'{elem}.jpeg'
                else:
                    file_name = f'{elem} {value["add_name"]}.jpeg'
                json_list.append({'file name': file_name, 'size': value["size"]})
                sorted_dict[file_name] = picture_dict[elem][0]['url_picture']
        return json_list, sorted_dict


# 552934290
