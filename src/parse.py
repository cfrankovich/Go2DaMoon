minlat = 9999.0 
maxlat = -9999.0 
minlon = 9999.0 
maxlon = -9999.0 


for i, line in enumerate(open('prec.csv', 'r')):
    s = line.split(',')
    print(f'\rCurrently on line: {i}', end='')
    minlat = min(float(s[0]), minlat)
    maxlat = max(float(s[0]), maxlat)
    minlon = min(float(s[1]), minlon)
    maxlon = max(float(s[1]), maxlon)

print('\n')
print(f'MinLat: {minlat}')
print(f'MaxLat: {maxlat}')
print(f'MinLon: {minlon}')
print(f'MaxLon: {maxlon}')

