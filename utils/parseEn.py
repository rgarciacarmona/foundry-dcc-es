import json
import fileinput
import pandas
import re
import translators as ts

# requires 
# pandas
# translators

def parse_line(line, dictionary):
    print(line)
    if line == "{" or line =="}" or line==" ":
        return;
    
    splitted = line.split(":", 2);
    key   = splitted[0].replace('"', '')
    value = splitted[1][1:-1].replace('"', '')
    dictionary[key] = value
    
def generate_dict(lines):
    dictionary = dict()
    for line in lines:
        parse_line(line.strip(), dictionary)
    return dictionary

def translate(en):
   matches = re.findall(r'{(.+?)}',en)
   translated = "";
   if not matches:
       try:
           translated = ts.server.google(en, from_language='en', to_language='es')
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
                   translated += ts.server.google(en, from_language='en', to_language='es')
               except:
                   translated += chunk 
           else:
               translated += chunk;
           translated += " " + match + " ";
           last = matchPos + len(match)
           
   return translated
           
print("PARSING ####")
print("Generating ENG dict")
en_dict = generate_dict(fileinput.input(['en.json'], encoding="utf-8"))
print("Generating ES dict")
es_dict = generate_dict(fileinput.input(['es.json'], encoding="utf-8"))
print("COMBINING ####")
combined = list()
for key,en_value in en_dict.items():
    es_value = es_dict.get(key)
    if (es_value == None):
        es_value = translate(en_value)
    print("ES: " + es_value)
    combined.append({'key': key, 'en' : en_value, 'es' : es_value})

print("WRITING XLSX ####")
df = pandas.DataFrame(combined).to_excel("excel.xlsx")  
