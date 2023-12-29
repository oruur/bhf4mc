import cv2, os, json
import numpy as np


class HFUtil(dict):
    def __init__(self, filename=None, width=16, xshift=0, yshift=0):
        self.width = width
        self.hangul = [(0x1100, 0x1113), (0x1161, 0x1176), (0x11A8, 0x11C3), (0x3131, 0x3164), (0xAC00, 0xD7A4)]
        if filename and os.path.isfile(filename):
            self.read(filename, xshift, yshift)


    def read(self, filename, xshift=0, yshift=0, range=(0, 0xFFFF)):
        """
        Read glyphs in unifont hex or bdf file and convert it to a dictionary.
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
                        if range[0] <= code < range[1]: self.setdefault(code, glyph)


    def rearange_base(self):
        """
        Rearrange base in group by code to group by variation or vice versa.
        """
        gbc = 0xF000
        gbv = 0xF100
        table = [(52, [0]), (19, [0, 2, 1, 3, 5, 4]), (21, [0, 2, 1]), (27, [0])]

        for m, n in table:
            for i in n:
                for j in range(m):
                    if gbv+j in self:
                        self[gbc+i+j*len(n)] = self[gbv+j]
                    elif gbc+i+j*len(n) in self:
                        self[gbv+j] = self[gbc+i+j*len(n)]
                gbv += m
            gbc += m*len(n)


    def compose_syllable(self, code):
        """
        Compose a glyph of a Hangul syllable using base glyphs.
        """
        c = code - 0xAC00
        initial, medial, final = c//28//21, c//28%21, c%28

        # Select initial consonant
        if medial in [ 9, 10, 11, 14, 15, 16, 19]:  initial += 19*1 # ㅘ,ㅙ,ㅚ,ㅝ,ㅞ,ㅟ,ㅢ
        if medial in [ 8, 12, 13, 17, 18]:          initial += 19*2 # ㅗ,ㅛ,ㅜ,ㅠ,ㅡ
        if medial in [13, 14, 15, 16, 17] or final: initial += 19*3 # ㅜ,ㅝ,ㅞ,ㅟ,ㅠ
        glyph = int(self[0xF134+initial], 16)

        # Select and overlay medial vowel
        if final == 4: medial += 21*1 # ㄴ
        elif final:    medial += 21*2
        glyph |= int(self[0xF1A6+medial], 16)

        # Select and overlay final consonant
        if final:
            if medial%21 in [1, 3, 5, 7, 10, 15]: # ㅐ,ㅒ,ㅔ,ㅖ,ㅙ,ㅞ
                glyph |= int(self[0xF1E4+final], 16) >> 1
            else:
                glyph |= int(self[0xF1E4+final], 16)

        return f'{glyph:064X}'


    def get(self, code, default=32*'0'):
        """
        Return a glyph of a char with code.
        """
        if code in self: return self[code]
        elif self.hangul[0][0] <= code < self.hangul[0][1]: return self[code-self.hangul[0][0]+0xF15A]
        elif self.hangul[1][0] <= code < self.hangul[1][1]: return self[code-self.hangul[1][0]+0xF1A6]
        elif self.hangul[2][0] <= code < self.hangul[2][1]: return self[code-self.hangul[2][0]+0xF1E5]
        elif self.hangul[3][0] <= code < self.hangul[3][1]: return self[code-self.hangul[3][0]+0xF101]
        elif self.hangul[4][0] <= code < self.hangul[4][1]: return self.compose_syllable(code)
        else: return default


    def export_hex(self, filename, text=[]):
        """
        Export glyphs data to unifont hex file.
        """
        self.read(filename)
        codes = [ord(i) for j in text for i in j] if text else self.keys()

        with open(filename, 'w') as f:
            for code in sorted(codes):
                f.write(f'{code:04X}:{self.get(code)}\n')


    def export_bdf(self, filename, text=[]):
        """
        Export glyphs data to bdf font file.
        """
        self.read(filename)
        codes = [ord(i) for j in text for i in j] if text else self.keys()

        with open(filename, 'w') as f:
            f.write('STARTFONT 2.1\nFONT Font\nSIZE 16 75 75\nFONTBOUNDINGBOX 16 16 0 -2\n')
            f.write('STARTPROPERTIES 5\nPIXEL_SIZE 16\nPOINT_SIZE 160\nSPACING "C"\n')
            f.write(f'FONT_ASCENT 14\nFONT_DESCENT 2\nENDPROPERTIES\nCHARS {len(self)}\n')

            for code in sorted(codes):
                glyph = self.get(code)
                w = len(glyph)//16
                f.write(f'STARTCHAR U+{code:04X}\nENCODING {code}')
                f.write(f'\nSWIDTH {240*w} 0\nDWIDTH {4*w} 0\nBBX {4*w} 16 0 -2\nBITMAP\n')
                f.write('\n'.join([f'{glyph}'[i:i+4] for i in range(0, 16*w, w)]))
                f.write('\nENDCHAR\n')

            f.write('ENDFONT\n')


    def bitmap(self, code):
        """
        Return bitmap of a char in numpy array.
        """
        glyph = self.get(code)
        w = len(glyph)//4
        bitmap = np.array([int(b) for b in f'{int(glyph,16):0{16*w}b}'], dtype=np.uint8).reshape(16, w)

        if 8 <= self.width < 16:
            bitmap = bitmap[:,:(self.width+1//2) if code < 0x100 else self.width]

        elif self.width < 8 and code != 32: # variable width
            nonzero = np.sum(bitmap, axis=0)
            nonzero[1:] += nonzero[:-1] // 9
            nonzero = np.nonzero(nonzero)[0]
            bitmap = np.pad(bitmap[:,nonzero[0]:1+nonzero[-1]], ((0, 0), (0, self.width)))

        return bitmap


    def export_png(self, filename, text=[], linespace=0, rgba=False):
        """
        Generate png image with sample text using glyphs data.
        """
        if not text:
            text = [chr(c) for c in self.keys()]
            text = [''.join(text[i:i+16]) for i in range(0, len(text), 16)]

        plane = []
        for line in text:
            if (line):
                line = [self.bitmap(ord(char)) for char in line.strip('\n')]
                plane.append(np.concatenate(line, axis=1))
            else:
                plane.append(np.zeros((8, 1), dtype=np.uint8))

        width = max([len(p[0]) for p in plane])
        for i in range(len(plane)):
            plane[i] = np.pad(plane[i], (((linespace+1)//2, linespace//2), (0, width-len(plane[i][0]))))

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
            if datafile.endswith('.png'):
                provider = {'type': 'bitmap', 'file': f'minecraft:font/{datafile}', 'ascent': 7}
                provider['chars'] = []
                for line in text:
                    if (line):
                        provider['chars'].append(line.strip())
            else:
                provider = {'type': 'unihex', 'hex_file': f'minecraft:font/{datafile[:-4]}.zip'}
                provider['size_overrides'] = []
                for i, j in self.hangul:
                    provider['size_overrides'].append({'from': chr(i), 'to': chr(j-1), 'left': 1, 'right': 15})

            json.dump({'providers': [provider]}, f, indent='\t', separators=(',', ': '))
