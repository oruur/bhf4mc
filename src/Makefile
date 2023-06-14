all: ../BetterHanFont.zip

hex: ../bin/hfutil hanbase-bold.bdf hanbase-regular.bdf
	../bin/hfutil -i hanbase-bold.bdf -o hanbase-bold.hex
	../bin/hfutil -i hanbase-regular.bdf -o hanbase-regular.hex

png: ../bin/hfutil hanbase-bold.bdf hanbase-regular.bdf
	../bin/hfutil -y1 -i hanbase-bold.bdf -o ../doc/base-bold.png
	../bin/hfutil -y1 -i hanbase-regular.bdf -o ../doc/base-regular.png
	../bin/hfutil -y1 -s2 -c 2350 -i hanbase-bold.bdf -o ../doc/han2350-bold.png
	../bin/hfutil -y1 -s1 -c 2350 -i hanbase-regular.bdf -o ../doc/han2350-regular.png
	../bin/hfutil -x1 -s2 -c ../doc/example.txt -i hanbase-bold.bdf -o ../doc/example-bold.png
	../bin/hfutil -s1 -w16 -c ../doc/example.txt -i hanbase-regular.bdf -o ../doc/example-regular.png

hangul.png: ../bin/hfutil hanbase-bold.bdf
	../bin/hfutil -s2 -c 11250 -i hanbase-bold.bdf -o hangul.png -j default.json

hangul.hex: ../bin/hfutil hanbase-regular.bdf
	../bin/hfutil -s1 -c 11250 -i hanbase-regular.bdf -o hangul.hex -j unifont.json

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
