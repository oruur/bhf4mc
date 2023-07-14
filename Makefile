all:
	cd font && make all
	cp font/BoldHanFont.zip ./
	cp font/BetterHanFont.zip ./

clean:
	cd font && make clean
