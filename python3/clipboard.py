from PIL import ImageGrab, Image
import time
import win32clipboard as w32c

test_no = '44'

folder_name = 'test'

count = 7

def monitor(interval_sec):
	pre_seq = None

	def read():
		img = ImageGrab.grabclipboard()
		if img != None:
			global count
			filename = folder_name + '\\' + test_no + '_'  + format(count, '03') +  ".png"
			img.save(filename)
			print(filename)
			count += 1
	while True:
		seq = w32c.GetClipboardSequenceNumber()

		if pre_seq == None:
			pre_seq = seq
		elif pre_seq != seq:
			data = read()
			pre_seq = seq

		time.sleep(interval_sec)

def main():
	print("testNo = " + test_no)
	monitor(1)

if __name__ == "__main__":
	main()