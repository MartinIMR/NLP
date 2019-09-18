def get_lemmas_dictionary(file_name):
    file = open(file_name, encoding = "latin-1")
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    lem_pos = {}
    for line in lines:
        if line != "":
            words = line.split() #List with splited line
            #words = [w.strip() for w in words]
            t = words[0]
            value = words[-1]
            pos = words[-2][0].lower()
            t = t.replace("#","")
            key = t + " " + pos
            lem_pos[key] = value
    return lem_pos


def save_ldict(lemmas):
    from pickle import dump
    output = open('lemmas.pkl',"wb")
    dump(lemmas,output, -1) #mete bytes en archivo nuestro diccionario de lemmas
    output.close()
   
if __name__=='__main__':
    fname = "./generate.txt" #ruta archivo lemmas
    lemmas = get_lemmas_dictionary(fname)
    save_ldict(lemmas)
