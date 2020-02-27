# Custom Utilities For the Project

def ExtractDICOM(folder_path="C:/Users/user/user/101Projects/Cancer Detection/DataMini"):
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

    extraction_path = "C:/Users/user/user/101Projects/Cancer Detection/DataMiniExtracted"
    print("Main Folder Path is : ",folder_path,"\n")
    def Extractor(folder_path,dir_space=0):
        PNG = False; #nonlocal writer; nonlocal fieldnames;
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

def ProcessDICOM(folder_path="/content/DataMiniProstateX2",output_path="/content/DataMiniX2Converted",Nifti=True):
    try :
        import os
        import traceback
        if Nifti == True :
            import dicom2nifti
            import SimpleITK as sitk
        elif Nifti != True:
            import cv2
            import pydicom as dicom
        import shutil
    except ModuleNotFoundError:
        tb = (traceback.format_exc()).split("ModuleNotFoundError:")
        print("ModuleNotFoundError : ",tb[1])
        tb = tb[1].split('\'')
        print("Attempting to Handle this Error. Hang Tight !!")  #Error is : tb[1]
        os.system('cmd /k "pip install {}"'.format(tb[1]))
        print("\nDONE.Trying to Import Again.")
        ProcessDICOM(folder_path,output_path,Nifti)
    except Exception as exp:
        print("---- !! IMPORT ERROR [custom_utilities.ProcessDICOM()] !! ----\n",exp,"\n---------- ---------------------------------------- ----------\n")

    print("Main Folder Path is : ",folder_path,"\n")

    def DICOMExtractor(folder_path,dir_space=0):
        PNG = False; #nonlocal writer; nonlocal fieldnames;
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

    def DICOM2Nifti(folder_path,dir_space=0):
      if os.path.isdir(folder_path):
        print(' |   '*dir_space,'├──',os.path.basename(folder_path)," >> ") #└──
        next_path = os.listdir(folder_path)
        for i,path in enumerate(next_path):
            next_path[i] = os.path.join(folder_path,path)
        for i,further_path in enumerate(next_path):
            DICOM2Nifti(further_path,(dir_space+1))

      elif os.path.isfile(folder_path):
        if '.dcm' in os.path.basename(folder_path):
          try:
            folder_path = os.path.dirname(folder_path)
            output_path = folder_path.replace("DataMiniProstateX2","DataMiniX2Converted")     #string.replace(old, new, count)
            if os.path.exists(output_path) == False:
              os.makedirs(output_path)  #Recursive os.mkdir to create Dirs in MultiLevel which os.mkdir fails to do
            dicom2nifti.convert_directory(folder_path,output_path,compression=False)
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
              print("---- !! IMPORT ERROR [custom_utilities.ProcessDICOM.DICOM2Nifti()-Try Block During DICOM to Nifti] !! ----\n",exp,"\n---------- ---------------------------------------- ----------\n")
              #traceback.format_exc()
              #print(sys.exc_info()[1])
              #print(sys.last_value)
              #traceback.print_exception(etype=sys.last_type,value=sys.last_value,tb=sys.last_traceback)

        elif '.mhd' in os.path.basename(folder_path):
          try:
            #print(' |   '*dir_space,' ** ',os.path.basename(folder_path)," **")
            img = sitk.ReadImage(folder_path)
            output_path = folder_path.replace("DataMiniProstateX2","DataMiniX2Converted")     #string.replace(old, new, count)
            output_path = output_path.replace(".mhd",".nii")
            if os.path.exists(os.path.dirname(output_path)) == False:
              os.makedirs(os.path.dirname(output_path))  #Recursive os.mkdir to create Dirs in MultiLevel which os.mkdir fails to do
            sitk.WriteImage(img,output_path)
          except Exception as exp:
            print("---- !! IMPORT ERROR [custom_utilities.ProcessDICOM.DICOM2Nifti()-Try Block During MHD to Nifti] !! ----\n",exp,"\n---------- ---------------------------------------- ----------\n")
        else:
          original = folder_path
          folder_path = folder_path.replace("DataMiniProstateX2","DataMiniX2Converted")
          if os.path.exists(os.path.dirname(folder_path)) == False:
              os.makedirs(os.path.dirname(folder_path))
          shutil.copyfile(original,folder_path)
          print(' |   '*dir_space,' ** ',os.path.basename(folder_path)," ** [Copied to the Output Folder]")
          #pass

      else:
        print("!! Cannot Determine Path Type !! : ",folder_path)

    if Nifti == True:
      print("\n\t\t==== ** ==== Performing DICOM TO NIFTI ==== ** ====\n")
      DICOM2Nifti(folder_path)
    elif Nifti == False:
      print("\n\t\t==== ** ==== Performing DICOM Extraction ==== ** ====\n")
      DICOMExtractor(folder_path)
    else :
      print("\n\t====  !! Invalid DICOM Processing !!  ====\n")

    print("\n\t\t==== ** ==== Extraction Sucessfully Completed ==== ** ====\n")

def mean(a):
    return sum(a) / len(a)

def smoothslices(inputarray, HM_SLICES):
    import numpy as np
    slices = inputarray.copy()
    #print(len(slices))
#         chunk_sizes = math.ceil(len(slices3) / HM_SLICES)
#         new_slices = []
#         for slice_chunk in chunks(slices3, chunk_sizes):
#             slice_chunk = list(map(mean, zip(*slice_chunk)))
#             new_slices.append(slice_chunk)

    if len(slices) == HM_SLICES-1:
        #print(slices.shape)
        #print(slices[HM_SLICES-2].shape)
        slices = np.append(slices,
                           np.reshape(slices[HM_SLICES-2], (1,slices[HM_SLICES-2].shape[0], slices[HM_SLICES-2].shape[1], slices[HM_SLICES-2].shape[2])),
                           axis=0)
#         print(slices.shape)

#     if len(new_slices) == HM_SLICES-2:
#         new_slices.append(new_slices[-1])
#         new_slices.append(new_slices[-1])

    if len(slices) > HM_SLICES:
#         print(slices[HM_SLICES-1:len(slices)].shape)
#         print(np.mean(slices[HM_SLICES-1:len(slices)], axis=0).shape)
#         print(slices[HM_SLICES-1].shape)
        slices[HM_SLICES-1] = np.mean(slices[HM_SLICES-1:len(slices)], axis=0)

    #print(slices[:HM_SLICES].shape)
    return slices[:HM_SLICES]

