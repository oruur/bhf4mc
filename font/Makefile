PATH=../util:/usr/bin

all: images BetterHanFont.zip BolderHanFont.zip

hex: Makefile base-bolder.bdf base-regular.bdf ../util/hfutil ../util/hfutil.py
	hfutil base-bolder.bdf base-bolder.hex
	hfutil base-regular.bdf base-regular.hex

images: Makefile base-bolder.bdf base-regular.bdf ../util/hfutil ../util/hfutil.py
	hfutil -y-1 -c basegbv base-bolder.bdf ../images/base-bolder.png
	hfutil -y 1 -c basegbv base-regular.bdf ../images/base-regular.png
	hfutil -y-1 -c han1764 base-bolder.bdf ../images/han1764-bolder.png
	hfutil -y 1 -c han1764 base-regular.bdf ../images/han1764-regular.png
	hfutil -y-1 -c han2350 base-bolder.bdf ../images/han2350-bolder.png
	hfutil -y 1 -c han2350 base-regular.bdf ../images/han2350-regular.png
	hfutil -y-1 -c example.txt base-bolder.bdf ../images/example-bolder.png
	hfutil -y 1 -c example.txt base-regular.bdf ../images/example-regular.png

BetterHanFont.zip: Makefile base-bolder.bdf base-regular.bdf ../util/hfutil ../util/hfutil.py
	mkdir -p assets/minecraft/font/include
	mkdir -p assets/minecraft/textures/font
	rm -f hangul.hex hangul.png assets/minecraft/font/hangul.zip
	hfutil -x-1 -c han11250 base-bolder.bdf hangul.png -j default.json
	hfutil -c han11250 base-regular.bdf hangul.hex -j unifont.json
	cp *.json assets/minecraft/font/include/
	cp hangul.png assets/minecraft/textures/font/
	zip -r assets/minecraft/font/hangul.zip hangul.hex
	zip -r BetterHanFont.zip assets/minecraft/font/include/default.json
	zip -r BetterHanFont.zip assets/minecraft/font/include/unifont.json
	zip -r BetterHanFont.zip assets/minecraft/font/hangul.zip
	zip -r BetterHanFont.zip assets/minecraft/textures/font/hangul.png
	zip -r BetterHanFont.zip pack.mcmeta

BolderHanFont.zip: Makefile base-bolder.bdf ../util/hfutil ../util/hfutil.py
	mkdir -p assets/minecraft/font/include
	rm -f hangul.hex hangul.png assets/minecraft/font/hangul.zip
	hfutil -c full base-bolder.bdf hangul.hex -j unifont.json
	cp unifont.json assets/minecraft/font/include/
	zip -r assets/minecraft/font/hangul.zip hangul.hex
	zip -r BolderHanFont.zip assets/minecraft/font/include/unifont.json
	zip -r BolderHanFont.zip assets/minecraft/font/hangul.zip
	zip -r BolderHanFont.zip pack.mcmeta

clean:
	rm -fr assets
	rm -f *.bak *.hex *.json *.png *.zip
