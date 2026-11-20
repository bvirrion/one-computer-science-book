import csv

line = "1,The Silent Code,Fatou Dalewell,2002,mystery,65"
print(line.split(","))

tricky = '81,"Salt, Sand and Sea",Mara Quill,2019,nature,210'
print(tricky.split(","))
for fields in csv.reader([tricky]):
    print(fields)
