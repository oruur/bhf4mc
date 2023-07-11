PATH=../util:/usr/bin

all: ../BetterHanFont.zip

hex: ../util/hfutil ../util/hfutil.py hanbase-bold.bdf hanbase-short.bdf hanbase-regular.bdf
	hfutil -i hanbase-bold.bdf -o hanbase-bold.hex
	hfutil -i hanbase-short.bdf -o hanbase-short.hex
	hfutil -i hanbase-regular.bdf -o hanbase-regular.hex

images: ../util/hfutil ../util/hfutil.py hanbase-bold.bdf hanbase-short.bdf hanbase-regular.bdf
	hfutil -y1 -i hanbase-bold.bdf -o ../images/base-bold.png
	hfutil -y1 -i hanbase-short.bdf -o ../images/base-short.png
	hfutil -y1 -i hanbase-regular.bdf -o ../images/base-regular.png
	hfutil -y1 -t han1764 -i hanbase-bold.bdf -o ../images/han1764-bold.png
	hfutil -y1 -t han1764 -i hanbase-short.bdf -o ../images/han1764-short.png
	hfutil -y1 -t han1764 -i hanbase-regular.bdf -o ../images/han1764-regular.png
	hfutil -y1 -t han2350 -i hanbase-bold.bdf -o ../images/han2350-bold.png
	hfutil -y1 -t han2350 -i hanbase-short.bdf -o ../images/han2350-short.png
	hfutil -y1 -t han2350 -i hanbase-regular.bdf -o ../images/han2350-regular.png
	hfutil -y1 -t example.txt -i hanbase-bold.bdf -o ../images/example-bold.png
	hfutil -y1 -t example.txt -i hanbase-short.bdf -o ../images/example-short.png
	hfutil -y1 -t example.txt -i hanbase-regular.bdf -o ../images/example-regular.png

hangul.png: ../util/hfutil ../util/hfutil.py hanbase-bold.bdf
	hfutil -t han11250 -i hanbase-bold.bdf -o hangul.png -j default.json

hangul.hex: ../util/hfutil ../util/hfutil.py hanbase-regular.bdf
	hfutil -w15 -t han11250 -i hanbase-regular.bdf -o hangul.hex -j unifont.json

../BetterHanFontRegular.zip: pack.mcmeta hangul.hex
	mkdir -p assets/minecraft/font/include
	mkdir -p assets/minecraft/textures/font
	rm -f BetterHanFont.zip assets/minecraft/font/hangul.zip
	cp unifont.json assets/minecraft/font/include/
	zip -r assets/minecraft/font/hangul.zip hangul.hex
	zip -r ../BetterHanFontRegular.zip pack.mcmeta
	zip -r ../BetterHanFontRegular.zip assets/minecraft/font/include/unifont.json
	zip -r ../BetterHanFontRegular.zip assets/minecraft/font/hangul.zip

../BetterHanFontBold.zip: pack.mcmeta hangul.png
	mkdir -p assets/minecraft/font/include
	mkdir -p assets/minecraft/textures/font
	cp default.json assets/minecraft/font/include/
	cp hangul.png assets/minecraft/textures/font/
	zip -r ../BetterHanFontBold.zip pack.mcmeta
	zip -r ../BetterHanFontBold.zip assets/minecraft/font/include/default.json
	zip -r ../BetterHanFontBold.zip assets/minecraft/textures/font/hangul.png

../BetterHanFont.zip: ../BetterHanFontRegular.zip ../BetterHanFontBold.zip
	zip -r ../BetterHanFont.zip pack.mcmeta
	zip -r ../BetterHanFont.zip assets/minecraft/font/include/unifont.json
	zip -r ../BetterHanFont.zip assets/minecraft/font/include/default.json
	zip -r ../BetterHanFont.zip assets/minecraft/font/hangul.zip
	zip -r ../BetterHanFont.zip assets/minecraft/textures/font/hangul.png

clean:
	rm -fr assets
	rm -f *.bak *.hex *.json *.png *.zip
