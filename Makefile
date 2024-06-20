all:
	cd font && make all
	cp font/BetterHanFont.zip ./
	cp font/BolderHanFont.zip ./

clean:
	rm -f *.zip
	cd font && make clean
