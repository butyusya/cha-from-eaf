file_name = input()
with open(file_name+".cha", "r", encoding="UTF-8") as f:
    raw = f.read()
corr = dict(zip('-абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ',
                "— a b v g d e jo zh z i j k l m n o p r s t u f x ts ch sh shch ^ y ' æ ju ja A B V G D E JO ZH Z I J "
                "K L M N O P R S T U F X TS CH SH HSCH Y Æ JU JA".split()))
for char in corr:
    raw = raw.replace(char, corr[char])
with open(file_name+".cha", "w", encoding="UTF-8") as f:
    f.write(raw)
