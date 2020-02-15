# Custom Utilities Developed by NabinAdhikari674
def ExtractDICOM(folder_path="C:/Users/nabin/Nabin/101Projects/Cancer Detection/DataMini"):
    try :
        import pydicom as dicom
        import PIL
        import matplotlib.pyplot as plt
        import os
        import cv2
        import pandas as pd
        import csv
        import shutil
    except Exception as exp:
        print("---- !! IMPORT ERROR [custom_utilities.ExtractDICOM()] !! ----\n",exp,"\n---------- ---------------------------------------- ----------\n")

    extraction_path = "C:/Users/nabin/Nabin/101Projects/Cancer Detection/DataMiniExtracted"
    print("Main Folder Path is : ",folder_path,"\n")
    def Extractor(folder_path,dir_space=0):
        PNG = False
        if os.path.isdir(folder_path):
            print(' |   '*dir_space,'├──',os.path.basename(folder_path)," >> ") #└──
            next_path = os.listdir(folder_path)
            for i,path in enumerate(next_path):
                next_path[i] = os.path.join(folder_path,path)
            for i,further_path in enumerate(next_path):
                Extractor(further_path,(dir_space+1))
        elif os.path.isfile(folder_path):
            #image_path = os.path.dirname(folder_path)
            try:
                ds = dicom.dcmread(folder_path)
                pixel_array_numpy = ds.pixel_array
                if PNG == False:
                    folder_path = folder_path.replace('.dcm', '.jpg')
                else:
                    folder_path = folder.replace('.dcm', '.png')
                folder_path = folder_path.replace("DataMini","DataMiniExtracted")     #string.replace(old, new, count)
                if os.path.exists(os.path.dirname(folder_path)) == False:
                    os.makedirs(os.path.dirname(folder_path))  #Recursive os.mkdir to create Dirs in MultiLevel which os.mkdir fails to do
                cv2.imwrite(folder_path,pixel_array_numpy)
                #print("Sucessfull Write to  : ",folder_path)
            except dicom.errors.InvalidDicomError:
                original = folder_path
                folder_path = folder_path.replace("DataMini","DataMiniExtracted")
                if os.path.exists(os.path.dirname(folder_path)) == False:
                    os.makedirs(os.path.dirname(folder_path))
                shutil.copyfile(original,folder_path)
                print(' |   '*dir_space,' ** ',os.path.basename(folder_path)," **")
                #pass
            except Exception as exp:
                print(exp)
                #traceback.format_exc()
                #print(sys.exc_info()[1])
                #print(sys.last_value)
                #traceback.print_exception(etype=sys.last_type,value=sys.last_value,tb=sys.last_traceback)

        else:
            print("!! Cannot Determine Path Type !! : ",folder_path)
    Extractor(folder_path)
    print("\n\t\t==== ** ==== Extraction Sucessfully Completed ==== ** ====\n")
