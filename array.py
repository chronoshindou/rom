import numpy as np
import re
list = np.array(["A","B","C","D","E","F","G","H","I"])

print(list.reshape(3,3))

a_tag = '<a href="/db/monsters/71006/" title="Rotar Zairo - Added by Guest at 13.12.2018 13:08:27 UTC+1"><img style="vertical-align: middle; width: 40px;" src="//s01.cdn.roguard.net/content/img/icons/monsters/goblin_helicopter_mini.png"></a>'
ch = re.findall('title="\w+ \w+',a_tag)
print ch