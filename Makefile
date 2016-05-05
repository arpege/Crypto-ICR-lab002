all: e

e: 
	./medivac file1.txt file2.txt

d:
	./medivac -d medfile.medivac ./out/

install:
	rm -f /usr/local/bin/medivac
	cp ./medivac /usr/local/bin/medivac