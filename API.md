# REST API for CiHui

## Authentication
Public access to the API not currently supported.

## Lists
The API supports:
- GET
- POST

### POST
Parameters
- title - name of the list to be created (or updated)
- words - List of words, where each word is a list of character, pinyin and definition.

For example:

``` python
import requests
payload = {'title': 'Script List', 
           'words': [[u'大', 'dà', 'big'], ]}

r = requests.post('http://localhost:5000/api/list',
                  data=json.dumps(payload),
                  auth=('user', 'secret'))
```