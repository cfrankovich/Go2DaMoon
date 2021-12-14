minlat = 9999.0 
maxlat = -9999.0 
minlon = 9999.0 
maxlon = -9999.0 
maxheight = -9999
minheight = 9999
minslope = 9999
maxslope = -9999

for i, line in enumerate(open('../data/lunardata.csv', 'r')):
    s = line.split(',')
    print(f'\rCurrently on line: {i}', end='')
    minlat = min(float(s[0]), minlat)
    maxlat = max(float(s[0]), maxlat)
    minlon = min(float(s[1]), minlon)
    maxlon = max(float(s[1]), maxlon)
    maxheight = max(float(s[2]), maxheight)
    minheight = min(float(s[2]), minheight)
    maxslope = max(float(s[3]), maxslope)
    minslope = min(float(s[3]), minslope)

print('\n')
print(f'MinLat: {minlat}')
print(f'MaxLat: {maxlat}')
print(f'MinLon: {minlon}')
print(f'MaxLon: {maxlon}')
print(f'MaxHeight: {maxheight}')
print(f'MinHeight: {minheight}')
print(f'MaxSlope: {maxslope}')
print(f'MinSlope: {minslope}')

