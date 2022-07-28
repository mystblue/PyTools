from PIL import ImageGrab, Image
import time
import win32clipboard as w32c

def monitor(interval_sec):
	pre_seq = None

	def read():
		img = ImageGrab.grabclipboard()
		if img != None:
			img.save('img.png')
	while True:
		seq = w32c.GetClipboardSequenceNumber()

		if pre_seq == None:
			pre_seq = seq
		elif pre_seq != seq:
			data = read()
			pre_seq = seq

		time.sleep(interval_sec)

def main():
	monitor(1)

if __name__ == "__main__":
	main()