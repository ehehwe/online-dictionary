import requests
from bs4 import BeautifulSoup
import time


# this app translates words
# german-turkish and turkish-german
# it shows the article and the type of the word whether it is a verb or adverb etc.
# it tracks dates and saves the search history on a text file
# it is also possible to add notes among with your searches by just adding a plus mark "+" before your search


def find_def(word):
    output = []

    r = requests.get("https://tr.bab.la/sozluk/almanca-turkce/" + word)
    soup = BeautifulSoup(r.content, "html.parser")

    sonuclar = soup.find_all("div", attrs={"class": "quick-result-entry"})

    for sonuc in sonuclar:
        try:
            sol = sonuc.find("a", attrs={"class": "babQuickResult"}).text
            a = str(sol).strip()

            orta = sonuc.find("span", attrs={"class": "suffix"}).text
            b = str(orta).strip()

            sag = sonuc.find("ul", attrs={"class": "sense-group-results"}).text
            c = str(sag).strip().replace("\n", ", ")
            mylist = [c]

            output.append(a + " " + b + " : " + ''.join(str(e) for e in mylist))
        except:
            pass

    return output


def langenscheidt(word):
    output = ""
    if len(word) < 2:
        return output
    try:
        r = requests.get("https://tr.langenscheidt.com/almanca-turkce/" + word)
        soup = BeautifulSoup(r.content, "html.parser")

        anlam = soup.find("span", attrs={"class": "btn-inner"}).text  
        aranan = soup.find("h5").text
        aranan_artikel = soup.find("span", attrs={"class": "abbr"}).text[-1]
        dic = {"f": "dis.", "m":"er.", "n": "no."}

        liste = ["f", "n", "m"]
        if aranan_artikel in liste:
            output = ("%s {%s} :%s " % (aranan, dic.get(aranan_artikel), anlam)) 
        else:
            output = ("%s :%s" % (aranan, anlam))
    except:
        pass
    return output



def check_date():
    global zaman
    zaman = time.localtime()
    # print("%d/%d/%d %d:%d" % (zaman[2], zaman[1], zaman[0], zaman[3], zaman[4]))
    today = "%d/%d/%d" % (zaman[2], zaman[1], zaman[0])

    tarihler = open("tarihler.txt", "r")
    try:
        lastline = tarihler.readlines()[-1]
    except:
        lastline = "olumsuz"
    tarihler.close()
    if lastline == today:
        return 1
    else:
        tarihler = open("tarihler.txt", "a")
        tarihler.write("\n" + today)
        tarihler.close()


def write(arama):
    file = open("kelimeler.txt", "a")

    if check_date() != 1:
        file.write("\n\n\n\n\n\n\n\n-->%d/%d/%d %d:%d\n" % (zaman[2], zaman[1], zaman[0], zaman[3], zaman[4]))

    if str(arama).startswith("+"):
        file.write(str(arama[1:]) + "\n\n")
        print("")

    else:
        elementler = find_def(arama)
        if elementler != []:
            for element in elementler:
                print(element)
                file.write(element + "\n")
            file.write("\n")
        else:
            elementler = langenscheidt(arama)
            if elementler != "":
                print(elementler)
                file.write(elementler + "\n\n")
        print("")
       
    file.close()


while True:
    arama = input(" kelime gir: ")
    if arama == "0":
        break
    if arama == "":
        continue
    write(arama)
