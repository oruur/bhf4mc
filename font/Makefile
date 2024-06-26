PATH=../util:/usr/bin

all: base-bolder.hex base-regular.hex BetterHangulFont.zip

base-bolder.hex: base-bolder.bdf Makefile ../util/hfutil ../util/hfutil.py
	rm -f base-bolder.bdf.bak
	hfutil base-bolder.bdf base-bolder.hex

base-regular.hex: base-regular.bdf Makefile ../util/hfutil ../util/hfutil.py
	rm -f base-regular.bdf.bak
	hfutil base-regular.bdf base-regular.hex

BetterHangulFont.zip: Makefile pack.mcmeta pack.txt base-bolder.hex ../util/hfutil ../util/hfutil.py
	mkdir -p assets/minecraft/font/include
	rm -f pack.png hangul.png hangul.hex assets/minecraft/font/hangul.zip
	hfutil -y-1 -c pack.txt base-bolder.hex pack.png
	hfutil -c full base-bolder.hex hangul.hex -j unifont.json
	cp unifont.json assets/minecraft/font/include/
	zip -r assets/minecraft/font/hangul.zip hangul.hex
	zip -r BetterHangulFont.zip assets/minecraft/font/include/unifont.json
	zip -r BetterHangulFont.zip assets/minecraft/font/hangul.zip
	zip -r BetterHangulFont.zip pack.mcmeta
	zip -r BetterHangulFont.zip pack.png

clean:
	rm -fr assets
	rm -f *.bak *.json *.png *.zip
