import cv2, os, json, argparse
import numpy as np


def importGlyphs(filename, base={}, xshift=0, yshift=0):
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
                    base.setdefault(code, glyph)
    return base


def composeChar(code, base, shift=0):
    """
    Compose a glyph of a Hangul char in Unicode plane 0 using the base glyphs.
    """
    # Hangul Jamo
    if   0x1100 <= code < 0x1113: return base[code-0x1100+0x134]
    elif 0x1161 <= code < 0x1176: return base[code-0x1161+0x1A6]
    elif 0x11A8 <= code < 0x11C3: return base[code-0x11A8+0x1E5]

    # Hangul Compatibility Jamo
    elif 0x3131 <= code < 0x3164: return base[code-0x3130+0x100]

    # Hangul Syllables
    elif 0xAC00 <= code < 0xD7A4:
        c = code - 0xAC00
        initial, medial, final = c//28//21, c//28%21, c%28

        # Select initial consonant
        if medial in [9, 10, 11, 14, 15, 16, 19]:   initial += 19*1 # ㅘ,ㅙ,ㅚ,ㅝ,ㅞ,ㅟ,ㅢ
        if medial in [8, 12, 13, 17, 18]:           initial += 19*2 # ㅗ,ㅛ,ㅜ,ㅠ,ㅡ
        if medial in [13, 14, 15, 16, 17] or final: initial += 19*3 # ㅜ,ㅝ,ㅞ,ㅟ,ㅠ
        glyph = base[0x134+initial]

        # Select and overlay medial vowel
        if final == 4: medial += 21*1   # ㄴ
        elif final:    medial += 21*2
        glyph |= base[0x1A6+medial]

        # Select and overlay final consonant
        if final:
            if medial%21 not in [1, 3, 5, 7, 10, 15]: shift = 0     # ㅐ,ㅒ,ㅔ,ㅖ,ㅙ,ㅞ
            glyph |= base[0x1E4+final] >> shift

    return glyph


def convertBase(base, method, shift=0):
    """
    Convert base glyphs data to base with different grouping or glyphs of
    entire Hangul jamos and syllables.
    """
    if method in ['gbc2gbv', 'gbv2gbc']:  # gbc: group by code, gbv: group by variation
        old = list(base.values())
        new = old[:]
        table = [(52,19,6),(53,19,6),(54,19,6),(55,19,6),(56,19,6),(57,19,6),(166,21,3),(167,21,3),(168,21,3)]
        s = 52
        for start, size, step in table:
            if method == 'gbc2gbv': new[s:s+size] = old[start:start+size*step:step]
            if method == 'gbv2gbc': new[start:start+size*step:step] = old[s:s+size]
            s += size
        base = {code+0x100: new[code] for code in range(len(new))}

    elif method:
        hangul11250  = list(range(0x11A8, 0x11C3))
        hangul11250 += list(range(0x3131, 0x3164))
        hangul11250 += list(range(0xAC00, 0xD7A4))
        base = {code: composeChar(code, base, shift) for code in hangul11250}

    return base


def exportHEX(filename, glyphs):
    """
    Generate unifont hex file from glyphs data.
    """
    glyphs = importGlyphs(filename, glyphs)

    with open(filename, 'w') as f:
        for key, value in sorted(glyphs.items()):
            if key < 0x100:
                f.write(f'{key:04X}:{value:032X}\n')
            else:
                f.write(f'{key:04X}:{value:064X}\n')


def exportBDF(filename, glyphs):
    """
    Generate bdf font file from glyphs data.
    """
    glyphs = importGlyphs(filename, glyphs)

    with open(filename, 'w') as f:
        f.write('STARTFONT 2.1\nFONT Font\nSIZE 16 75 75\nFONTBOUNDINGBOX 16 16 0 -2\n')
        f.write('STARTPROPERTIES 5\nPIXEL_SIZE 16\nPOINT_SIZE 160\nSPACING "C"\n')
        f.write(f'FONT_ASCENT 14\nFONT_DESCENT 2\nENDPROPERTIES\nCHARS {len(glyphs)}\n')

        for key, value in sorted(glyphs.items()):
            f.write(f'STARTCHAR U+{key:04X}\nENCODING {key}')
            if key < 0x100:
                f.write('\nSWIDTH 500 0\nDWIDTH 8 0\nBBX 8 16 0 -2\nBITMAP\n')
                f.write('\n'.join([f'{value:032X}'[i:i+2] for i in range(0, 32, 2)]))
            else:
                f.write('\nSWIDTH 960 0\nDWIDTH 16 0\nBBX 16 16 0 -2\nBITMAP\n')
                f.write('\n'.join([f'{value:064X}'[i:i+4] for i in range(0, 64, 4)]))
            f.write('\nENDCHAR\n')

        f.write('ENDFONT\n')


def makeBitmap(glyph, width=16):
    """
    Convert glyph data in large integer to bitmap data in numpy array.
    """
    if width and width <= 8:
        bitmap = np.array([int(b) for b in f'{glyph:0128b}'], dtype=np.uint8).reshape(16, 8)
    else:
        bitmap = np.array([int(b) for b in f'{glyph:0256b}'], dtype=np.uint8).reshape(16, 16)
        if width:
            bitmap = bitmap[:,:width]
        else:
            bitmap = np.pad(bitmap[:,:1+np.nonzero(np.any(bitmap, axis=0))[0][-1]], ((0, 0), (0, 2)))

    return bitmap


def exportPNG(filename, glyphs, cols=0, rows=0, width=16, rgba=False, text=None):
    """
    Generate an image containing cols*rows chars from glyphs data.
    """
    plane = []

    if text:
        glyphs[0x20] = 0
        for line in text.strip().split('\n'):
            if (line):
                line = [makeBitmap(glyphs[ord(c)], 8 if ord(c) < 0x100 else width) for c in line]
                plane.append(np.concatenate(line, axis=1))
            else:
                plane.append(np.zeros((16, 1), dtype=np.uint8))
        width = max([len(p[0]) for p in plane])
        for i in range(len(plane)):
            plane[i] = np.pad(plane[i], ((0, 2), (0, width-len(plane[i][0]))))

    else:
        glyphs = list(glyphs.values())
        for i in range(rows):
            line = []
            for j in range(cols):
                line.append(makeBitmap(glyphs[cols*i+j] if cols*i+j < len(glyphs) else 0))
            plane.append(np.concatenate(line, axis=1))

    plane = np.concatenate(plane)
    if rgba: cv2.imwrite(filename, 255 * cv2.merge([plane, plane, plane, plane]))
    else: cv2.imwrite(filename, 255 * (1-plane))


def createJSON(jsonfile, output, glyphs, cols, rows):
    """
    Create JSON file for Minecraft font resource pack.
    """
    with open(jsonfile, 'w') as f:
        provider = {}

        if output.endswith('.hex'):
            provider['type'] = 'unihex'
            provider['hex_file'] = f'minecraft:font/{output[:-4]}.zip'
            provider['size_overrides'] = [{
                        'from': chr(0x1100),
                        'to': chr(0xFF00),
                        'left': 0,
                        'right': 14
                    }]

        else:
            provider['type'] = 'bitmap'
            provider['file'] = f'minecraft:font/{output[:-4]}.png'
            provider['ascent'] = 8
            provider['chars'] = []
            for i in range(rows):
                provider['chars'].append('')
                for j in range(cols):
                    provider['chars'][-1] += chr(glyphs[cols*i+j] if cols*i+j < len(glyphs) else 0)

        json.dump({'providers': [provider]}, f, indent='\t', separators=(',', ': '))
