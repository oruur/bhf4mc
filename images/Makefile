all: bolder regular

bolder: base-bolder.png base-bolder.png han1764-bolder.png han2350-bolder.png example-bolder.png

regular: base-regular.png base-regular.png han1764-regular.png han2350-regular.png example-regular.png

base-bolder.png: Makefile ../font/base-bolder.hex ../util/hfutil ../util/hfutil.py
	hfutil -y-1 -c basegbv ../font/base-bolder.hex base-bolder.png

base-regular.png: Makefile ../font/base-regular.hex ../util/hfutil ../util/hfutil.py
	hfutil -y 1 -c basegbv ../font/base-regular.hex base-regular.png

han1764-bolder.png: Makefile ../font/base-bolder.hex ../util/hfutil ../util/hfutil.py
	hfutil -y-1 -c han1764 ../font/base-bolder.hex han1764-bolder.png

han1764-regular.png: Makefile ../font/base-regular.hex ../util/hfutil ../util/hfutil.py
	hfutil -y 1 -c han1764 ../font/base-regular.hex han1764-regular.png

han2350-bolder.png: Makefile ../font/base-bolder.hex ../util/hfutil ../util/hfutil.py
	hfutil -y-1 -c han2350 ../font/base-bolder.hex han2350-bolder.png

han2350-regular.png: Makefile ../font/base-regular.hex ../util/hfutil ../util/hfutil.py
	hfutil -y 1 -c han2350 ../font/base-regular.hex han2350-regular.png

example-bolder.png: Makefile example.txt ../font/base-bolder.hex ../util/hfutil ../util/hfutil.py
	hfutil -y-1 -l8 -c example.txt ../font/base-bolder.hex example-bolder.png

example-regular.png: Makefile example.txt ../font/base-regular.hex ../util/hfutil ../util/hfutil.py
	hfutil -y 1 -l8 -c example.txt ../font/base-regular.hex example-regular.png

clean:
	rm -f *-bolder.png *-regular.png
