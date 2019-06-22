import requests

with open('tags.txt','r') as f:
	content = f.readlines()
tags = [x.strip() for x in content]

for tag in tags:
	r = requests.get('http://3.19.61.141:8000/reddit/add_tag_reddit/?tag={}'.format(tag))
	print(r)
