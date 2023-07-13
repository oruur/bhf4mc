PATH=../util:/usr/bin

all: BoldHanFont.zip BetterHanFont.zip
	cp BoldHanFont.zip ../
	cp BetterHanFont.zip ../

hex: Makefile hanbase-bold.bdf hanbase-short.bdf hanbase-regular.bdf ../util/hfutil ../util/hfutil.py
	hfutil hanbase-bold.bdf hanbase-bold.hex
	hfutil hanbase-short.bdf hanbase-short.hex
	hfutil hanbase-regular.bdf hanbase-regular.hex

images: Makefile hanbase-bold.bdf hanbase-short.bdf hanbase-regular.bdf ../util/hfutil ../util/hfutil.py
	hfutil -y1 hanbase-bold.bdf ../images/base-bold.png
	hfutil -y1 hanbase-short.bdf ../images/base-short.png
	hfutil -y1 hanbase-regular.bdf ../images/base-regular.png
	hfutil -y1 -c han1764 hanbase-bold.bdf ../images/han1764-bold.png
	hfutil -y1 -c han1764 hanbase-short.bdf ../images/han1764-short.png
	hfutil -y1 -c han1764 hanbase-regular.bdf ../images/han1764-regular.png
	hfutil -y1 -c han2350 hanbase-bold.bdf ../images/han2350-bold.png
	hfutil -y1 -c han2350 hanbase-short.bdf ../images/han2350-short.png
	hfutil -y1 -c han2350 hanbase-regular.bdf ../images/han2350-regular.png
	hfutil -y1 -c example.txt hanbase-bold.bdf ../images/example-bold.png
	hfutil -y1 -c example.txt hanbase-short.bdf ../images/example-short.png
	hfutil -y1 -c example.txt hanbase-regular.bdf ../images/example-regular.png

BoldHanFont.zip: Makefile hanbase-bold.bdf pack.mcmeta ../util/hfutil ../util/hfutil.py
	mkdir -p assets/minecraft/font/include
	rm -f hangul.hex hangul.png assets/minecraft/font/hangul.zip
	hfutil -x-1 -y2 -c han11250 hanbase-bold.bdf hangul.hex -j unifont.json
	cp unifont.json assets/minecraft/font/include/
	zip -r assets/minecraft/font/hangul.zip hangul.hex
	zip -r BoldHanFont.zip pack.mcmeta
	zip -r BoldHanFont.zip assets/minecraft/font/include/unifont.json
	zip -r BoldHanFont.zip assets/minecraft/font/hangul.zip

BetterHanFont.zip: Makefile hanbase-bold.bdf hanbase-regular.bdf pack.mcmeta ../util/hfutil ../util/hfutil.py
	mkdir -p assets/minecraft/font/include
	mkdir -p assets/minecraft/textures/font
	rm -f hangul.hex hangul.png assets/minecraft/font/hangul.zip
	hfutil -c han11250 hanbase-bold.bdf hangul.png -j default.json
	hfutil -c han11250 hanbase-regular.bdf hangul.hex -j unifont.json
	cp default.json unifont.json assets/minecraft/font/include/
	cp hangul.png assets/minecraft/textures/font/
	zip -r assets/minecraft/font/hangul.zip hangul.hex
	zip -r BetterHanFont.zip pack.mcmeta
	zip -r BetterHanFont.zip assets/minecraft/font/include/default.json
	zip -r BetterHanFont.zip assets/minecraft/font/include/unifont.json
	zip -r BetterHanFont.zip assets/minecraft/font/hangul.zip
	zip -r BetterHanFont.zip assets/minecraft/textures/font/hangul.png

clean:
	rm -fr assets
	rm -f *.bak *.hex *.json *.png *.zip
