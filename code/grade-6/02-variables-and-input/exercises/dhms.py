total = int(input("Seconds: "))
days = total // 86400
hours = total % 86400 // 3600
minutes = total % 3600 // 60
seconds = total % 60
print(f"{days} days, {hours} h, {minutes} min, {seconds} s")
