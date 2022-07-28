import win32clipboard as w32c
import time

def monitor(interval_sec, onchange):
	pre_seq = None

	def read():
		try:
			w32c.OpenClipboard()
			return w32c.GetClipboardData()
		except Exception as ex:
			return ex
		finally:
			w32c.CloseClipboard()

	while True:
		seq = w32c.GetClipboardSequenceNumber()

		if pre_seq != seq:
			data = read()
			pre_seq = seq

			onchange(data)

		time.sleep(interval_sec)

def main():
	def onchange(data):
		if isinstance(data, Exception):
			print("Failed:", data)
		else:
			print("Clipboard:", data)

	monitor(2, onchange)

if __name__ == "__main__":
	main()