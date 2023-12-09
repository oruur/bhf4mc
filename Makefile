all:
	cd font && make all
	cp font/BetterHanFont.zip ./BetterHanFont-1.20.zip
	cp font/BolderHanFont.zip ./BolderHanFont-1.20.zip
	cp font/BetterHanFont.zip ./BetterHanFont-1.20.2.zip
	cp font/BolderHanFont.zip ./BolderHanFont-1.20.2.zip
	cp font/BetterHanFont.zip ./BetterHanFont-1.20.3.zip
	cp font/BolderHanFont.zip ./BolderHanFont-1.20.3.zip
	util/pack 15 && zip -r BetterHanFont-1.20.zip pack.mcmeta && rm pack.mcmeta
	util/pack 15 && zip -r BolderHanFont-1.20.zip pack.mcmeta && rm pack.mcmeta
	util/pack 18 && zip -r BetterHanFont-1.20.2.zip pack.mcmeta && rm pack.mcmeta
	util/pack 18 && zip -r BolderHanFont-1.20.2.zip pack.mcmeta && rm pack.mcmeta
	util/pack 22 && zip -r BetterHanFont-1.20.3.zip pack.mcmeta && rm pack.mcmeta
	util/pack 22 && zip -r BolderHanFont-1.20.3.zip pack.mcmeta && rm pack.mcmeta

clean:
	rm -f *.zip
	cd font && make clean
