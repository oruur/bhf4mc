import cv2, os, json
import numpy as np


class HFUtil:
    def __init__(self, filename, shift=0, xshift=0, yshift=0, width=16):
        self.data = {}
        self.shift = shift if shift else 0
        self.width = 16 if width == None else width
        self.read(filename, shift, xshift, yshift)
        self.range = [(0x1100, 0x1113), (0x1161, 0x1176), (0x11A8, 0x11C3), (0x3131, 0x3164), (0xAC00, 0xD7A4)]


    def read(self, filename, shift=0, xshift=0, yshift=0):
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
                        bitmap = line.strip()[5:]
                    if line.startswith('ENCODING'):
                        code = int(line[9:])
                        bitmap = ''
                    if len(line) in [3, 5]:
                        bitmap += line.strip()
                    if line.startswith('ENDCHAR') or line[4:5] == ':':
                        glyph = int(bitmap, 16)
                        if shift > 0: glyph >>=  shift
                        if shift < 0: glyph <<= -shift
                        self.data.setdefault(code, glyph)


    def compose_syllable(self, code):
        """
        Compose a glyph of a Hangul char in Unicode plane 0 using the base glyphs.
        """
        # Hangul Jamo
        if   self.range[0][0] <= code < self.range[0][1]: return self.data[code-self.range[0][0]+0x134]
        elif self.range[1][0] <= code < self.range[1][1]: return self.data[code-self.range[1][0]+0x1A6]
        elif self.range[2][0] <= code < self.range[2][1]: return self.data[code-self.range[2][0]+0x1E5]

        # Hangul Compatibility Jamo
        elif self.range[3][0] <= code < self.range[3][1]: return self.data[code-self.range[3][0]+0x101]

        # Hangul Syllables
        elif self.range[4][0] <= code < self.range[4][1]:
            c = code - self.range[4][0]
            initial, medial, final = c//28//21, c//28%21, c%28

            # Select initial consonant
            if medial in [9, 10, 11, 14, 15, 16, 19]:   initial += 19*1 # ㅘ,ㅙ,ㅚ,ㅝ,ㅞ,ㅟ,ㅢ
            if medial in [8, 12, 13, 17, 18]:           initial += 19*2 # ㅗ,ㅛ,ㅜ,ㅠ,ㅡ
            if medial in [13, 14, 15, 16, 17] or final: initial += 19*3 # ㅜ,ㅝ,ㅞ,ㅟ,ㅠ
            glyph = self.data[0x134+initial]

            # Select and overlay medial vowel
            if final == 4: medial += 21*1 # ㄴ
            elif final:    medial += 21*2
            glyph |= self.data[0x1A6+medial]

            # Select and overlay final consonant
            if final:
                if medial%21 in [1, 3, 5, 7, 10, 15]: # ㅐ,ㅒ,ㅔ,ㅖ,ㅙ,ㅞ
                    glyph |= self.data[0x1E4+final] >> self.shift
                else:
                    glyph |= self.data[0x1E4+final]

        return glyph


    def convert(self, method=''):
        """
        Convert base glyphs data to base with different grouping or glyphs of
        entire Hangul jamos and syllables (default: gbv2utf).
         * gbc2utf: base glyphs sorted in group by code to unicode
         * gbv2utf: base glyphs sorted in group by variation to unicode
         * gbc2gbv: base glyphs in group by code to group by variation
         * gbv2gbc: base glyphs in group by variation to group by code
        """
        if method == 'gbc2utf':
            self.convert('gbc2gbv')
            self.convert('gbv2utf')

        elif method in ['gbc2gbv', 'gbv2gbc']:
            old = [self.data[c] for c in range(0x134, 0x1E5)]
            new = old[:]
            first  = 0
            table  = [(i,      19, 6) for i in (0, 2, 1, 3, 5, 4)]
            table += [(i+19*6, 21, 3) for i in (0, 2, 1)]
            for start, size, step in table:
                if method == 'gbc2gbv': new[first:first+size] = old[start:start+size*step:step]
                if method == 'gbv2gbc': new[start:start+size*step:step] = old[first:first+size]
                first += size
            for c in range(19*6 + 21*3):
                self.data[c+0x134] = new[c]

        elif method:
            for start, stop in self.range:
                for code in range(start, stop): self.data[code] = self.compose_syllable(code)
            for code in range(0x0100, 0x1000):
                self.data.pop(code, None)


    def export_hex(self, filename):
        """
        Export glyphs data to unifont hex file.
        """
        self.read(filename)

        with open(filename, 'w') as f:
            for key, value in sorted(self.data.items()):
                if key < 0x100:
                    f.write(f'{key:04X}:{value:032X}\n')
                else:
                    f.write(f'{key:04X}:{value:064X}\n')


    def export_bdf(self, filename):
        """
        Export glyphs data to bdf font file.
        """
        self.read(filename)

        with open(filename, 'w') as f:
            f.write('STARTFONT 2.1\nFONT Font\nSIZE 16 75 75\nFONTBOUNDINGBOX 16 16 0 -2\n')
            f.write('STARTPROPERTIES 5\nPIXEL_SIZE 16\nPOINT_SIZE 160\nSPACING "C"\n')
            f.write(f'FONT_ASCENT 14\nFONT_DESCENT 2\nENDPROPERTIES\nCHARS {len(self.data)}\n')

            for key, value in sorted(self.data.items()):
                f.write(f'STARTCHAR U+{key:04X}\nENCODING {key}')
                if key < 0x100:
                    f.write('\nSWIDTH 500 0\nDWIDTH 8 0\nBBX 8 16 0 -2\nBITMAP\n')
                    f.write('\n'.join([f'{value:032X}'[i:i+2] for i in range(0, 32, 2)]))
                else:
                    f.write('\nSWIDTH 960 0\nDWIDTH 16 0\nBBX 16 16 0 -2\nBITMAP\n')
                    f.write('\n'.join([f'{value:064X}'[i:i+4] for i in range(0, 64, 4)]))
                f.write('\nENDCHAR\n')

            f.write('ENDFONT\n')


    def bitmap(self, code):
        """
        Return bitmap of a char in numpy array.
        """
        glyph = self.data.get(code, 0)

        if code < 0x100:
            bitmap = np.array([int(b) for b in f'{glyph:0128b}'], dtype=np.uint8).reshape(16, 8)
        else:
            bitmap = np.array([int(b) for b in f'{glyph:0256b}'], dtype=np.uint8).reshape(16, 16)

        if 0 < self.width < 16:
            bitmap = bitmap[:,:(self.width+1//2) if code < 0x100 else self.width]
        elif self.width <= 0 and code != 32 and code != 256: # variable width
            bitmap = np.pad(bitmap[:,:1+np.nonzero(np.any(bitmap, axis=0))[0][-1]], ((0, 0), (0, -self.width)))

        return bitmap


    def export_png(self, filename, text, linespace=0, rgba=False):
        """
        Export glyphs data to png file with text.
        """
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
        if filename.endswith('.bdf'): self.export_bdf(filename)
        if filename.endswith('.hex'): self.export_hex(filename)
        if filename.endswith('.png'): self.export_png(filename, text, linespace, rgba)


    def json(self, jsonfile, datafile, text):
        """
        Create JSON file for Minecraft font resource pack.
        """
        with open(jsonfile, 'w') as f:
            provider = {}

            if datafile.endswith('.hex'):
                provider['type'] = 'unihex'
                provider['hex_file'] = f'minecraft:font/{datafile[:-4]}.zip'
                provider['size_overrides'] = [{
                            'from': chr(0x1100),
                            'to': chr(0xFF00),
                            'left': 0,
                            'right': 14
                        }]
            else:
                provider['type'] = 'bitmap'
                provider['file'] = f'minecraft:font/{datafile[:-4]}.png'
                provider['ascent'] = 8
                provider['chars'] = []

                for line in text:
                    if (line):
                        provider['chars'].append(line.strip())

            json.dump({'providers': [provider]}, f, indent='\t', separators=(',', ': '))
