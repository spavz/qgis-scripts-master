import shapefile

sf = shapefile.Reader("C:/Users/visha/Downloads/Final Network_SHAPEFILES/Zones Complete/New_Zones.shp")
print(sf.bbox)

baseX = sf.bbox[0]
baseY = sf.bbox[1]

MULTIPLYING_SCALE_X = 10000
MULTIPLYING_SCALE_Y = 10000

scaled_coordinates = dict()

for shapeRecord in sf.shapeRecords():
    coordinates = shapeRecord.shape.__geo_interface__['coordinates'][0]
    zone_id = shapeRecord.record[0]

    scaled_coordinates[zone_id] = []
    for coordinate in coordinates:
        scaled_coordinates[zone_id].apppend((MULTIPLYING_SCALE_X * (coordinate[0] - baseX), MULTIPLYING_SCALE_Y * (coordinate[1] - baseY)))


for shapeRecord in sf.shapeRecords():
    print(shapeRecord.shape.__geo_interface__)
    print(shapeRecord.record)
    zone_id = shapeRecord.record[0]
    print(scaled_coordinates[zone_id])
    print()
    




# for shape in sf.shapes():
#     print(shape.points)

# for record in sf.records():
#     print(record)

# print(len(sf.shapes()))
# for coordinateId in range(len(coordinates)):
#     coordinates[coordinateId] = 


# for id in range(len(shapes)):
#     print(shapes(id).bbox)

#first feature of the shapefile
    # for coordinate in first['coordinates'][0]:
    #     if coordinate in cache:
    #         cacheHitCount += 1
    #     cache.add(coordinate)
    # print()
    # feature = shape.shapeRecords()[0]
    # print(first['coordinates'][0])



# for feature in shapes.shapeRecords():
#     first = feature.shape.__geo_interface__  
#     print(first) # (GeoJSON format)
#     print()

