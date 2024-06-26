all:
	cd font && make all
	cd images && make all
	cp font/BetterHangulFont.zip ./

clean:
	rm -f *.zip
	cd font && make clean
	cd images && make clean
