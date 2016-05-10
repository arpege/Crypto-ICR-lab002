all: e

e: 
	./medivac ~/.ssh/private.pem file1.txt file2.txt

d:
	./medivac -d ~/.ssh/private.pem medfile.medivac ./out/

install:
	rm -f /usr/local/bin/medivac
	cp ./medivac /usr/local/bin/medivac