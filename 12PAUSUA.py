import json


json_edukia = '{"id":1315301,"name":"Nire kanala","description":null,"latitude":"0.0",' \
       '"longitude":"0.0","created_at":"2021-03-01T10:34:38Z","elevation":null,' \
       '"last_entry_id":null,"public_flag":false,"url":null,"ranking":30,' \
       '"metadata":null,"license_id":0,"github_url":null,"tags":[],' \
       '"api_keys":[{"api_key":"D8QK4AKNNNRHDN8W","write_flag":true},{"api_key":"YD1U0C36VUL2X7V9","write_flag":false}]}'


hiztegia = json.loads(json_edukia)


kanala_id = hiztegia["id"]
write_api_key = hiztegia["api_keys"][0]["api_key"]