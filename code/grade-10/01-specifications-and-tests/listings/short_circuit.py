def loud(value):
    print("  evaluating loud(" + str(value) + ")")
    return value


print("False and loud(True):")
print(False and loud(True))
print("True and loud(False):")
print(True and loud(False))
print("True or loud(False):")
print(True or loud(False))
