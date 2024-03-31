import re
file_name = input()
with open(file_name+".txt", "r", encoding="UTF-8") as f:
    text = f.read()
text += "\n"
with open(file_name+".eaf", "r", encoding="UTF-8") as f:
    raw = f.read()
corr = dict(zip('-абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ',
                "— a b v g d e jo zh z i j k l m n o p r s t u f x ts ch sh shch ^ y ' æ ju ja A B V G D E JO ZH Z I J "
                "K L M N O P R S T U F X TS CH SH HSCH Y Æ JU JA".split()))
for char in corr:
    raw = raw.replace(char, corr[char])
time_slots = re.findall(r'<TIME_SLOT TIME_SLOT_ID="ts\d+" TIME_VALUE="\d+"/>', raw)
times = dict()
for t in time_slots:
    times["ts"+re.findall(r"\d+", t)[0]] = re.findall(r"\d+", t)[1]
allpeople = re.findall(r'LINGUISTIC_TYPE_REF="utterance"[\s\S]+?</TIER>', raw)
comments = dict()
if re.findall(r'LINGUISTIC_TYPE_REF="commentary"[\s\S]+?</TIER>', raw):
    commentary = re.findall(r'LINGUISTIC_TYPE_REF="commentary"[\s\S]+?</TIER>', raw)[0]
    comms = re.findall(r'<ANNOTATION>[\s\S]+?</ANNOTATION>', commentary)
    for comm in comms:
        start = re.findall(r'TIME_SLOT_REF1="(.+?)"', comm)[0]
        end = re.findall(r'TIME_SLOT_REF2="(.+?)"', comm)[0]
        words = re.findall(r'<ANNOTATION_VALUE>(.+?)</ANNOTATION_VALUE>', comm)[0]
        comments[(int(times[start]), int(times[end]))] = words
annotations = dict()
for person in allpeople:
    name = re.findall(r'PARTICIPANT="(.+?)"', person)[0]
    ans = re.findall(r'<ANNOTATION>[\s\S]+?</ANNOTATION>', person)
    for an in ans:
        start = re.findall(r'TIME_SLOT_REF1="(.+?)"', an)[0]
        end = re.findall(r'TIME_SLOT_REF2="(.+?)"', an)[0]
        words = re.findall(r'<ANNOTATION_VALUE>(.+?)</ANNOTATION_VALUE>', an)[0]
        annotations[(int(times[start]), int(times[end]))] = (name, words)
sort_ann = dict(sorted(annotations.items(), key=lambda item: item[0]))
for time, an in sort_ann.items():
    line = f'*{an[0]}:\t{an[1]}{str(time[0])}_{str(time[1])}\n'
    if time in comments:
        line += f'{comments[time]}\n'
    text += line
with open(file_name+".cha", "w", encoding="UTF-8") as f:
    f.write(text + "@End")
