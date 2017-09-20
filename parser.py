import json
from collections import defaultdict

'''
  images: picture info of each image
  info: SIND v1.0
  albums: info of each album
  type: story-in-sequence or description-in-isolation
  annotations: text info of each pics
'''

for dst in ['train', 'test', 'val']:
  img = {}
  albums = {}
  anno_sis = defaultdict(list)
  anno_dii = defaultdict(lambda: defaultdict(str))
  vist = defaultdict(dict)

  with open('data/%s.story-in-sequence.json' % dst, 'r') as file:
    data = json.load(file)

    for d in data['images']:
      img[d['id']] = d
    for d in data['albums']:
      albums[d['id']] = d

    for d in data['annotations']:
      anno_sis[d[0]['story_id']].append(d[0])
      
  with open('data/%s.description-in-isolation.json' % dst, 'r') as file:
    data = json.load(file)
    for d in data['annotations']:
      anno_dii[d[0]['photo_flickr_id']] = d[0]

  for key, value in anno_sis.items():
    vist[key] = {
      'title': albums[value[0]['album_id']]['title'],
      'description': albums[value[0]['album_id']]['description'],
      'data': [{
                'original_text_sis': v['original_text'],
                'text_sis': v['text'],
                'original_text_dii': anno_dii[v['photo_flickr_id']]['original_text'],
                'text_dii': anno_dii[v['photo_flickr_id']]['text'],
                'pic_id': v['photo_flickr_id'],
                'tags': img[v['photo_flickr_id']]['tags'],
               } for v in sorted(value, key = lambda x: x['worker_arranged_photo_order'])],
    }

  with open('data/%s.json' % dst, 'a') as file:
    for key, value in list(vist.items()):
      json.dump(value, file)
      file.write('\n')
