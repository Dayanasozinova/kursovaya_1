from os import path
import requests
from pprint import pprint
import json
from time import sleep
from tqdm import tqdm
for i in tqdm(range(2)):
  sleep(1)


class API_VK:
  def __init__(self,file_vk):
    with open(file_vk, 'r') as f:
      token = f.read().strip()
    self.token = token

  def get_photos(self):
    URL = 'https://api.vk.com/method/photos.get'
    params = {
      'owner_id': '552934290',
      'album_id': 'profile',
      'extended': '1', 
      'photo_sizes': '1', 
      'v':'5.131', 
      'access_token': self.token}
    res = requests.get(URL, params=params)
    global res_json
    res_json = res.json()

    data_list =[]
    for item in res_json['response']['items']:        
      data_dict = {}        
      size_list = []
      for size in item['sizes']:            
        p = size['height']*size['width']
        size_list.append(p)
            
      max_size = max(size_list)

      index = int(size_list.index(max_size))
       
      data_dict['file_name'] = str(item['likes']['count']) + '.jpg'
      data_dict['path'] = item['sizes'][index]['url']
      data_dict['size'] = item['sizes'][index]['type']
      data_list.append(data_dict)
        
    return data_list


class YaUploader:
  def __init__(self, file_ya):
    with open(file_ya, 'r') as f:
      token_ya = f.read().strip()
    self.token = token_ya

  def create_date(self, date):
    url_1 = "https://cloud-api.yandex.net/v1/disk/resources/"
    headers_1 = { "Accept": "application/json", "Authorization": "OAuth " + self.token}
    params_1 = {'path': date}
    r_1 = requests.put(url=url_1, params=params_1, headers=headers_1)
    res_1 = r_1.json()
    # pprint(json.dumps(res_1, sort_keys=True, indent=4, ensure_ascii=False))

  def upload (self, path, url):
    headers = {"Accept": "application/json", "Authorization": "OAuth " + self.token}        
    params = {'path': str(path), 'url': str(url)}        
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
    r = requests.post(url=url, params=params, headers=headers)
    res = r.json()
    # pprint(json.dumps(res, sort_keys=True, indent=4, ensure_ascii=False))

        

if __name__ == '__main__':
  file_vk = str(input('Введите файл, в котором храниться токен VK: '))
  
  login = API_VK(file_vk)                
  get_photos = login.get_photos()
    
  file_ya = str(input('Введите файл, в котором храниться токен Yandex Disk: ')) 
  
  uploader = YaUploader(file_ya)

  date = str(input('Введите название папки, в которой будут храниться фотографии из VK: '))
  uploader.create_date(date)

  i = 0
  for path in get_photos:
    i += 1  
    name = path['file_name']
    url = path['path']
    path_to_file = f'/{date}/{name}'
    result = uploader.upload(path_to_file, url)
    

  if i == len(get_photos):
    print('Все фотографии загружены)')
  else:
    print('Произошла какая-то ошибка. Свяжитесь с нами и мы постараемся вам помочь \nEmail: daanasozinova6@gmail.com')