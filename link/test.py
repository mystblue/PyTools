psp = "SBPS"
start = 534
middle = 539
end = 575

file_path = "test.txt"

buf = ""

buf += psp + " No" + str(start) + " から " + str(middle) + "\n"
count = middle + 1
buf += psp + " No" + str(count) + " から " + str(count + 2) + "\n"
count = count + 3
buf += psp + " No" + str(count) + " から " + str(count + 5) + "\n"
count = count + 6
buf += psp + " No" + str(count) + " から " + str(count + 2) + "\n"
count = count + 3
buf += psp + " No" + str(count) + " から " + str(count + 2) + "\n"
count = count + 3
buf += psp + " No" + str(count) + " から " + str(count + 2) + "\n"
count = count + 3
buf += psp + " No" + str(count) + " から " + str(count + 8) + "\n"
count = count + 9
buf += psp + " No" + str(count) + " から " + str(count + 2) + "\n"
count = count + 3
buf += psp + " No" + str(count) + " から " + str(count + 2) + "\n"
count = count + 3
buf += psp + " No" + str(count) + " から " + str(count + 2) + "\n"
count = count + 3

with open(file_path, "w", encoding="utf-8") as f:
    f.write(buf)
