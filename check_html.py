import sys

html = open('index.html').read()
errors = []

if '<script' not in html:
    errors.append('Missing <script> tag')
if '</html>' not in html:
    errors.append('Missing </html> closing tag')
if 'labs-grid' not in html:
    errors.append('Missing #labs-grid element')
if 'search-input' not in html:
    errors.append('Missing #search-input element')

if errors:
    print('index.html checks FAILED:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

print(f'index.html OK ({len(html):,} bytes, {html.count(chr(10))} lines)')
