# A number of seconds written as hours, minutes and seconds.
total = int(input("Seconds: "))
hours = total // 3600
rest = total % 3600
minutes = rest // 60
seconds = rest % 60
print(f"{hours}:{minutes}:{seconds}")
