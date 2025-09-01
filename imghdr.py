import os

def what(file, h=None):
    if h is None:
        with open(file, 'rb') as f:
            h = f.read(32)
    for type, test in tests:
        res = test(h, f)
        if res:
            return res
    return None

def test_jpeg(h, f):
    if h[6:10] in (b'JFIF', b'Exif'):
        return 'jpeg'

def test_png(h, f):
    if h.startswith(b'\211PNG\r\n\032\n'):
        return 'png'

def test_gif(h, f):
    if h[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif'

tests = [
    ('jpeg', test_jpeg),
    ('png', test_png),
    ('gif', test_gif),
]