"""Assemble index.html from src/atlas.src.html and the JSON files in data/."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'src', 'atlas.src.html'), encoding='utf-8').read()
for key, name in (('/*__GEO__*/null', 'geo.json'), ('/*__DATA__*/null', 'data.json'), ('/*__DATA2__*/null', 'data2.json')):
    assert key in src, key
    src = src.replace(key, open(os.path.join(ROOT, 'data', name), encoding='utf-8').read().strip())
cut = src.index('</style>') + len('</style>')
head, body = src[:cut], src[cut:]
page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="description" content="An illustrated, interactive map of Argentina\'s resources, trade and foreign investment, with sourced charts for the EC 391 country project.">\n'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}[hidden]{display:none!important}</style>\n'
        + head + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page)
print(f'index.html written ({len(page)/1024:.0f} KB)')
