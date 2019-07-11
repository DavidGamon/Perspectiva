import os
import sys
import cv2
import json
import numpy as np

path_to_analice = sys.argv[1]
listaDeArchivos = os.listdir(path_to_analice)

listaDeArchivosJSON = [jsonFile for jsonFile in listaDeArchivos if ".json" in jsonFile]

print(listaDeArchivosJSON)

counter = 0

export_path = path_to_analice + "/output/"

if not os.path.exists(export_path):
    os.mkdir(export_path)

for jsonFile in listaDeArchivosJSON:
    print('JSON File: {}'.format(counter))
    counter +=1
    list_of_points = []
    with open(path_to_analice+'/'+jsonFile) as currentFile :
        data = json.load(currentFile)
        path_to_current_file = data['asset']['path'].split(":")[1]
        
        export_file = export_path + data['asset']['path'].split("/")[-1]
        print("Path to image "+str(path_to_current_file))
        print("Points data "+str(data['regions'][0]['points']))

        points = data['regions'][0]['points']

        for point in points:
            x = float(point['x'])
            y = float(point['y'])
            #print(x)
            #print(y)
            list_of_points.append([x,y])

        print("Result "+str(list_of_points))

        image = cv2.imread(path_to_current_file)
        print(image.shape)
        cv2.imshow("Image",image)

        lienzoDestino = np.float32([[0,0], [250,0], [250,200], [0,200]])

		# For source points I'm grabbing the outer four detected corners
        extremosDeOrigen= np.float32(list_of_points)
		
		# Given extremosDeOrigenand lienzoDestino points, calculate the perspective transform matrix
        try:
            M = cv2.getPerspectiveTransform(extremosDeOrigen, lienzoDestino)
        except:
            print("Skipping image, is the input right?")
            continue

        output_image = cv2.warpPerspective(image, M,(250,200))

        cv2.imshow("Output",output_image)
        print(output_image.shape)
        cv2.waitKey(1)

        cv2.imwrite(export_file,output_image)
        print("\tSaved in file:"+export_file)
        print(" ---.---")
            

    