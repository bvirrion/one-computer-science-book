total = 0
count = 0
mark = float(input("Mark (-1 to stop): "))
while mark != -1:
    total = total + mark
    count = count + 1
    mark = float(input("Mark (-1 to stop): "))
print(f"{count} marks, average {total / count}")
