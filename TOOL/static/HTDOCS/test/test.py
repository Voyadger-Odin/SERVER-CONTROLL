from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

print()
print("Current Time is :", current_time)

#print('\n+'*100)

s = int(now.strftime('%S'))
m = int(now.strftime('%M'))
print(f'\n{s * m}')


print(12 / 0)
