import json

# возвращает list со всеми id
def GetAllId():
    ret = []
    file = open('json.json', 'r+')
    BD = json.load(file)
    file.close()
    for key in BD:
        ret.append(key)
        ret.sort()
    return ret


# возвращает dict с информацией о пользователи id или "error" если нет такого id
def GetInfo(id):
    file = open('json.json', 'r+')
    BD = json.load(file)
    file.close()
    if (str(id) in BD.keys()):
        return {
            "name": BD[str(id)]["name"],
            "tag": BD[str(id)]["tag"],
            "birth": BD[str(id)]["birth"],
            "gender": BD[str(id)]["gender"]
        }
    else:
        print("Неверный ID")
        return None
#добавляет запись
#при первом открытии считываем БД, при втором все удаляется из файла и записывается новая база
#при удалении и обновлении та жа схема
def AddInfo(id, name, birth=None, gender=None, tag=None):
    file = open('json.json', 'r+')
    BD = json.load(file)
    file.close()
    BD[id] = {"name": name, "birth": birth, "gender": gender, "tag": tag}
    file = open("json.json", "w")
    json.dump(BD, file, separators=(",", ":"))
    file.close()
    return None


def DelInfo(id):
    file = open('json.json', 'r+')
    BD = json.load(file)
    file.close()
    if (str(id) in BD.keys()):
        file = open("json.json", "w")
        BD.pop(str(id))
        json.dump(BD, file, separators=(",", ":"))
        file.close()
        return None
    else:
       print("error")
       return None


def UpdateInfo(id, name=None, birth=None, gender=None, tag=None):
    file = open('json.json', 'r+')
    BD = json.load(file)
    file.close()
    if (str(id) in BD.keys()):
             if not (name == None):
                BD[str(id)]["name"] = name
             if not (birth == None):
                BD[str(id)]["birth"] = birth
             if not (gender == None):
                BD[str(id)]["gender"] = gender
             if not (tag == None):
                BD[str(id)]["tag"] = tag

             file = open("json.json", "w")
             json.dump(BD, file, separators=(",", ":"))
             file.close()
             return None
    else:
        print("error")
        return None


