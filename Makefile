all: e

e: 
	./medivac.py ~/.ssh/private.pem file1.txt file2.txt

d:
	./medivac.py -d ~/.ssh/private.pem medfile.medivac ./out/
	
test:
	./test_suite.py

clean:
	rm -f ./medfile.medivac
	rm -f ./out/*

install:
	rm -f /usr/local/bin/medivac
	cp ./medivac.py /usr/local/bin/medivac