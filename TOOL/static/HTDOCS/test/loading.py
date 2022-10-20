import time


print()

size = 60
for i in range(size+1):
	time.sleep(0.05)
	print('\r', f'Loading: [{"="*i}{">" if (i<size) else "="}{" "*(size-i)}] {int((i/size*100))}%', end='')

print()
print('Loading compleated')


'''
frames = ['\\', '|', '/', '-']

frame = 0
while True:

	print('\r', f'Loading: {frames[frame]}', end='')

	frame += 1
	if (frame >= len(frames)):
		frame = 0
	time.sleep(0.2)
	
'''