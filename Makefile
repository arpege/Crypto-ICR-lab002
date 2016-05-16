all: e

e: 
	./medivac.py ~/.ssh/private.pem file1.txt file2.txt

d:
	./medivac.py -d ~/.ssh/private.pem medfile.medivac ./out/

install:
	rm -f /usr/local/bin/medivac
	cp ./medivac.py /usr/local/bin/medivac