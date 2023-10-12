import csv
import re
import googletrans
from googletrans import Translator

from polyglot.transliteration import Transliterator
transliterator = Transliterator(source_lang="hi", target_lang="en")
with open("readme.txt", "r") as in_file:
    lines = in_file.readlines()
open("transition.txt", "w").close()
translator = Translator()
d = 0

for line in lines:
    d = d+1
    if d%2==1:        
        line = line.replace(",,", "," )
        list = line.split(",")
        list[0].rstrip()
        first = list[0].split(" ")[-1]
        list[1].strip()
        second = list[1].split(":")[-1]
        tr = translator.translate(second,dest = 'en')
        second = tr.text
        
        #second = transliterator.transliterate(second)
        #print(second)
        flag = 0
        #print(list[2].split(":")[0])
        if list[2].split(":")[0]=="पिता का नाम " :
            third = list[2].split(":")[-1]
            fourth = ""
        else :
            fourth = list[2].split(":")[-1]
            third = ""

        tr3 = translator.translate(third,dest = 'en')
        tr4 = translator.translate(fourth,dest = 'en')
        third = tr3.text
        fourth = tr4.text
        fifth = list[3].split(":")[-1]
        seventh = list[4].split(":")[-1]
        sixth = list[4].split("लिंग")[0]
        sixth = sixth.split(":")[-1]
        sixth.rstrip()
        tr7 = translator.translate(seventh,dest = 'en')
        seventh = tr7.text
        with open('transition.txt', 'a') as f:

            f.write(format(first))
            f.write(',')
            f.write(format(second))
            f.write(',')
            f.write(format(third))
            f.write(',')
            f.write(format(fourth))
            f.write(',')
            f.write(format(fifth))
            f.write(',')
            f.write(format(sixth))
            f.write(',')
            f.write(format(seventh))
            f.write('\n')
        list.clear()

print(d)