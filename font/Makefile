PATH=../util:/usr/bin

all: images BoldHanFont.zip BetterHanFont.zip

hex: Makefile base-bold.bdf base-short.bdf base-regular.bdf ../util/hfutil ../util/hfutil.py
	hfutil base-bold.bdf base-bold.hex
	hfutil base-short.bdf base-short.hex
	hfutil base-regular.bdf base-regular.hex

images: Makefile base-bold.bdf base-short.bdf base-regular.bdf ../util/hfutil ../util/hfutil.py
	hfutil -y-1 -c basegbv base-bold.bdf ../images/base-bold.png
	hfutil -y 1 -c basegbv base-short.bdf ../images/base-short.png
	hfutil -y 1 -c basegbv base-regular.bdf ../images/base-regular.png
	hfutil -y-1 -c han1764 base-bold.bdf ../images/han1764-bold.png
	hfutil -y 1 -c han1764 base-short.bdf ../images/han1764-short.png
	hfutil -y 1 -c han1764 base-regular.bdf ../images/han1764-regular.png
	hfutil -y-1 -c han2350 base-bold.bdf ../images/han2350-bold.png
	hfutil -y 1 -c han2350 base-short.bdf ../images/han2350-short.png
	hfutil -y 1 -c han2350 base-regular.bdf ../images/han2350-regular.png
	hfutil -y-1 -c example.txt base-bold.bdf ../images/example-bold.png
	hfutil -y 1 -c example.txt base-short.bdf ../images/example-short.png
	hfutil -y 1 -c example.txt base-regular.bdf ../images/example-regular.png

BoldHanFont.zip: Makefile base-bold.bdf pack.mcmeta ../util/hfutil ../util/hfutil.py
	mkdir -p assets/minecraft/font/include
	rm -f hangul.hex hangul.png assets/minecraft/font/hangul.zip
	hfutil -y-1 -c full base-bold.bdf hangul.hex -j unifont.json
	cp unifont.json assets/minecraft/font/include/
	zip -r assets/minecraft/font/hangul.zip hangul.hex
	zip -r BoldHanFont.zip pack.mcmeta
	zip -r BoldHanFont.zip assets/minecraft/font/include/unifont.json
	zip -r BoldHanFont.zip assets/minecraft/font/hangul.zip

BetterHanFont.zip: Makefile base-bold.bdf base-regular.bdf pack.mcmeta ../util/hfutil ../util/hfutil.py
	mkdir -p assets/minecraft/font/include
	mkdir -p assets/minecraft/textures/font
	rm -f hangul.hex hangul.png assets/minecraft/font/hangul.zip
	hfutil -x-1 -y-1 -c han11250 base-bold.bdf hangul.png -j default.json
	hfutil -c han11250 base-regular.bdf hangul.hex -j unifont.json
	cp *.json assets/minecraft/font/include/
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
