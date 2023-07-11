import cv2, os, json
import numpy as np


class HFUtil:
    def __init__(self, filename, shift=0, xshift=0, yshift=0, width=16):
        self.data = {}
        self.shift = shift
        self.width = width
        self.read(filename, shift, xshift, yshift)
        self.range = [(0x1100, 0x1113), (0x1161, 0x1176), (0x11A8, 0x11C3), (0x3131, 0x3164), (0xAC00, 0xD7A4)]


    def read(self, filename, shift=0, xshift=0, yshift=0, range=(0, 0xFFFF)):
        """
        Import glyphs in unifont hex or bdf format and convert it to an array of
        large integers.
        """
        shift = 0
        if xshift: shift += xshift
        if yshift: shift -= yshift * 16

        if filename and os.path.isfile(filename):
            with open(filename, 'r') as f:
                for line in f.readlines():
                    if line[4:5] == ':':
                        code = int(line[0:4], 16)
                        glyph = line.strip()[5:]
                    if line.startswith('ENCODING'):
                        code = int(line[9:])
                        glyph = ''
                    if len(line) in [3, 5]:
                        glyph += line.strip()
                    if line.startswith('ENDCHAR') or line[4:5] == ':':
                        if shift > 0: glyph = f'{int(glyph,16)>> shift:0{len(glyph)}X}'
                        if shift < 0: glyph = f'{int(glyph,16)<<-shift:0{len(glyph)}X}'
                        if range[0] <= code < range[1]: self.data.setdefault(code, glyph)


    def compose_syllable(self, code):
        """
        Compose a glyph of a Hangul char in Unicode plane 0 using the base glyphs.
        """
        # Hangul Jamo
        if   self.range[0][0] <= code < self.range[0][1]: return self.data[code-self.range[0][0]+0xF134]
        elif self.range[1][0] <= code < self.range[1][1]: return self.data[code-self.range[1][0]+0xF1A6]
        elif self.range[2][0] <= code < self.range[2][1]: return self.data[code-self.range[2][0]+0xF1E5]

        # Hangul Compatibility Jamo
        elif self.range[3][0] <= code < self.range[3][1]: return self.data[code-self.range[3][0]+0xF101]

        # Hangul Syllables
        elif self.range[4][0] <= code < self.range[4][1]:
            c = code - self.range[4][0]
            initial, medial, final = c//28//21, c//28%21, c%28

            # Select initial consonant
            if medial in [9, 10, 11, 14, 15, 16, 19]:   initial += 19*1 # ㅘ,ㅙ,ㅚ,ㅝ,ㅞ,ㅟ,ㅢ
            if medial in [8, 12, 13, 17, 18]:           initial += 19*2 # ㅗ,ㅛ,ㅜ,ㅠ,ㅡ
            if medial in [13, 14, 15, 16, 17] or final: initial += 19*3 # ㅜ,ㅝ,ㅞ,ㅟ,ㅠ
            glyph = int(self.data[0xF134+initial], 16)

            # Select and overlay medial vowel
            if final == 4: medial += 21*1 # ㄴ
            elif final:    medial += 21*2
            glyph |= int(self.data[0xF1A6+medial], 16)

            # Select and overlay final consonant
            if final:
                if medial%21 in [1, 3, 5, 7, 10, 15]: # ㅐ,ㅒ,ㅔ,ㅖ,ㅙ,ㅞ
                    glyph |= int(self.data[0xF1E4+final], 16) >> self.shift
                else:
                    glyph |= int(self.data[0xF1E4+final], 16)

        return f'{glyph:064X}'


    def convert(self):
        """
        Convert base glyphs data to entire Hangul jamos and syllables.
        """
        gbc = 0xF000
        gbv = 0xF100
        table = [(52, [0]), (19, [0, 2, 1, 3, 5, 4]), (21, [0, 2, 1]), (27, [0])]

        for m, n in table:
            for i in n:
                for j in range(m):
                    if gbv+j in self.data:
                        self.data[gbc+i+j*len(n)] = self.data[gbv+j]
                    elif gbc+i+j*len(n) in self.data:
                        self.data[gbv+j] = self.data[gbc+i+j*len(n)]
                gbv += m
            gbc += m*len(n)

        for start, stop in self.range:
            for code in range(start, stop): self.data[code] = self.compose_syllable(code)


    def export_hex(self, filename, text=[]):
        """
        Export glyphs data to unifont hex file.
        """
        self.read(filename)
        codes = [ord(i) for j in text for i in j] if text else self.data.keys()

        with open(filename, 'w') as f:
            for c in sorted(codes):
                f.write(f'{c:04X}:{self.data.get(c,0)}\n')


    def export_bdf(self, filename, text=[]):
        """
        Export glyphs data to bdf font file.
        """
        self.read(filename)
        codes = [ord(i) for j in text for i in j] if text else self.data.keys()

        with open(filename, 'w') as f:
            f.write('STARTFONT 2.1\nFONT Font\nSIZE 16 75 75\nFONTBOUNDINGBOX 16 16 0 -2\n')
            f.write('STARTPROPERTIES 5\nPIXEL_SIZE 16\nPOINT_SIZE 160\nSPACING "C"\n')
            f.write(f'FONT_ASCENT 14\nFONT_DESCENT 2\nENDPROPERTIES\nCHARS {len(self.data)}\n')

            for c in sorted(codes):
                glyph = self.data.get(c, 0)
                w = len(glyph)//16
                f.write(f'STARTCHAR U+{c:04X}\nENCODING {c}')
                f.write(f'\nSWIDTH {240*w} 0\nDWIDTH {4*w} 0\nBBX {4*w} 16 0 -2\nBITMAP\n')
                f.write('\n'.join([f'{glyph}'[i:i+4] for i in range(0, 16*w, w)]))
                f.write('\nENDCHAR\n')

            f.write('ENDFONT\n')


    def bitmap(self, code):
        """
        Return bitmap of a char in numpy array.
        """
        glyph = self.data.get(code, f'{0:032b}')
        w = len(glyph)//4
        bitmap = np.array([int(b) for b in f'{int(glyph,16):0{16*w}b}'], dtype=np.uint8).reshape(16, w)

        if 8 <= self.width < 16:
            bitmap = bitmap[:,:(self.width+1//2) if code < 0x100 else self.width]
        elif self.width < 8 and code != 32 and code != 256: # variable width
            bitmap = np.pad(bitmap[:,:1+np.nonzero(np.any(bitmap, axis=0))[0][-1]], ((0, 0), (0, self.width)))

        return bitmap


    def export_png(self, filename, text=[], linespace=0, rgba=False):
        """
        Export glyphs data to png file with text.
        """
        if not text:
            text = [chr(c) for c in self.data.keys()]
            text = [''.join(text[i:i+16]) for i in range(0, len(text), 16)]

        plane = []
        for line in text:
            if (line):
                line = [self.bitmap(ord(char)) for char in line.rstrip()]
                plane.append(np.concatenate(line, axis=1))
            else:
                plane.append(np.zeros((16, 1), dtype=np.uint8))

        width = max([len(p[0]) for p in plane])
        for i in range(len(plane)):
            plane[i] = np.pad(plane[i], ((linespace//2, (linespace+1)//2), (0, width-len(plane[i][0]))))

        plane = np.concatenate(plane)
        if rgba:
            cv2.imwrite(filename, 255 * cv2.merge([plane, plane, plane, plane]))
        else:
            cv2.imwrite(filename, 255 * (1-plane))


    def export(self, filename, text=[], linespace=0, rgba=False):
        """
        Export glyphs data to bdf, hex, or png file.
        """
        if filename.endswith('.bdf'): self.export_bdf(filename, text)
        if filename.endswith('.hex'): self.export_hex(filename, text)
        if filename.endswith('.png'): self.export_png(filename, text, linespace, rgba)


    def json(self, jsonfile, datafile, text):
        """
        Create JSON file for Minecraft font resource pack.
        """
        with open(jsonfile, 'w') as f:
            if datafile.endswith('.hex'):
                provider = {'type': 'unihex', 'hex_file': f'minecraft:font/{datafile[:-4]}.zip'}
                provider['size_overrides'] = []
                for i, j in self.range[2:]:
                    size_overrides = {'from': chr(i), 'to': chr(j), 'left': 0, 'right': self.width-1}
                    provider['size_overrides'].append(size_overrides)
            else:
                provider = {'type': 'bitmap', 'file': f'minecraft:font/{datafile[:-4]}.png', 'ascent': 8}
                provider['chars'] = []
                for line in text:
                    if (line):
                        provider['chars'].append(line.strip())

            json.dump({'providers': [provider]}, f, indent='\t', separators=(',', ': '))
