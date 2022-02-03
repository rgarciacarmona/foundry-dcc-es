import json
import fileinput
import pandas
import re
from google_trans_new import google_translator

# requires 
# pandas
# googletrans 4.0.0rc1, had to tweak it to fix gender specific translation issues
# https://github.com/ssut/py-googletrans/issues/260#issuecomment-752342998

dict = list();
translator = google_translator(timeout=10)

def translate(en):
   matches = re.findall(r'{(.+?)}',en)
   translated = "";
   if not matches:
       try:
           translated = translator.translate(en, src='en', dest='es').text
       except:
           translated = en
   else:
       
       last = 0;
       for match in matches:
           match = "{" + match + "}"
           matchPos = en.find(match);
           chunk = en[last:matchPos]
           if (not chunk.isspace()) and (len(chunk) > 0):
               try:
                   translated += translator.translate(chunk, src='en', dest='es').text
               except:
                   translated += chunk 
           else:
               translated += chunk;
           translated += " " + match + " ";
           last = matchPos + len(match)
           
   return translated
           

def parse(line):
    if line == "{" or line =="}":
        return;
    
    splitted = line.split(":", 2);
    key = splitted[0].replace('"', '')
    print("KEY: " + key)
    en  = splitted[1][1:-1].replace('"', '')
    print("EN: ." + en + ".")
    
    es = translate(en)       
    print("ES: " + es)
    dict.append({'key': key, 'en' : en, 'es' : es})
   
   
print("PARSING")
for line in fileinput.input(['en.json']):
    parse(line.strip())

print("WRITING XLSX")
df = pandas.DataFrame(dict).to_excel("excel.xlsx")  
