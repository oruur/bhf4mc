all:
	cd font && make all
	cp font/BetterHanFont.zip ./BetterHanFont-1.20.1.zip
	cp font/BolderHanFont.zip ./BolderHanFont-1.20.1.zip
	cp font/BetterHanFont.zip ./BetterHanFont-1.20.2.zip
	cp font/BolderHanFont.zip ./BolderHanFont-1.20.2.zip
	cp font/BetterHanFont.zip ./BetterHanFont-1.20.4.zip
	cp font/BolderHanFont.zip ./BolderHanFont-1.20.4.zip
	cp font/BetterHanFont.zip ./BetterHanFont-1.20.6.zip
	cp font/BolderHanFont.zip ./BolderHanFont-1.20.6.zip
	util/pack 15 && zip -r BetterHanFont-1.20.1.zip pack.mcmeta && rm pack.mcmeta
	util/pack 15 && zip -r BolderHanFont-1.20.1.zip pack.mcmeta && rm pack.mcmeta
	util/pack 18 && zip -r BetterHanFont-1.20.2.zip pack.mcmeta && rm pack.mcmeta
	util/pack 18 && zip -r BolderHanFont-1.20.2.zip pack.mcmeta && rm pack.mcmeta
	util/pack 22 && zip -r BetterHanFont-1.20.4.zip pack.mcmeta && rm pack.mcmeta
	util/pack 22 && zip -r BolderHanFont-1.20.4.zip pack.mcmeta && rm pack.mcmeta
	util/pack 32 && zip -r BetterHanFont-1.20.6.zip pack.mcmeta && rm pack.mcmeta
	util/pack 32 && zip -r BolderHanFont-1.20.6.zip pack.mcmeta && rm pack.mcmeta

clean:
	rm -f *.zip
	cd font && make clean
