# PreProcessing of the Raw Data
#Working Dir : C:/Users/user/user/101Projects/Cancer Detection/sources/preProcessing.py
#Data Dir : C:/Users/user/user/DataForML/Data For ProstateX2/(Train/Test)
for Importbuffer in range (1,11):
    try:
        print("Importing Packages... ",end=" ")
        import cv2
        from dipy.align.imaffine import (transform_centers_of_mass,
                                      AffineMap,
                                      MutualInformationMetric,
                                      AffineRegistration)
        from dipy.align.transforms import (TranslationTransform3D,
                                        RigidTransform3D,
                                        AffineTransform3D)
        from dipy.data import fetch_stanford_hardi, read_stanford_hardi
        from dipy.data.fetcher import fetch_syn_data, read_syn_data
        from dipy.viz import regtools
        import matplotlib.pyplot as plt
        import nibabel as nib
        import numpy as np
        import os
        import pandas as pd
        import pickle
        import pydicom
        import SimpleITK as sitk
        print("All Packages Sucessfully Imported.\n")
        break
    except ModuleNotFoundError:
        tb = (traceback.format_exc()).split("ModuleNotFoundError:")
        print("ModuleNotFoundError : ",tb[1])
        tb = tb[1].split('\'')
        print("Attempting to Handle this Error. Hang Tight !!")  #Error is : tb[1]
        os.system('cmd /k "pip install {}"'.format(tb[1]))
        print("\nDONE.Trying to Import Again.")
    except Exception as exp:
        print("---- !! IMPORT ERROR [preProcessing.py] !! ----\n",exp,"\n---------- ---------------------------------------- ----------\n")
    if Importbuffer > 9:
        print("---- !! IMPORT ERROR [preProcessing.py] !! ----\n")
        print("Couldn't Import All of the Packages even on Multiple Retries !!")
        print("\n---------- ---------------------------------------- ----------\n")

dataFolder = 'C:/Users/user/user/DataForML/Data For ProstateX2/'

print("Reading the Labels from Provided CSV Files.",end=" ")
labels_df = pd.read_csv('C:/Users/user/user/DataForML/Data For ProstateX2/Train/Train_Info/ProstateX-2-Findings-Train.csv', index_col=0)
details_df = pd.read_csv('C:/Users/user/user/DataForML/Data For ProstateX2/Train/Train_Info/ProstateX-2-Images-Train.csv', index_col=0)
details_df['patient']=details_df.index
details_df = details_df[(details_df['Name'] == "t2_tse_tra0") | (details_df['Name'] == "t2_tse_tra_Grappa30")]
print("## DONE\n")
#print(labels_df)

print("==== Creating Dictionaries for Labels and Details of MRI Images ... ====")
labelsDict= {}
regionDict= {}
CoorDicts = {}
voxelSpace = {}
patientcase = {}
data_dir = 'C:/Users/user/user/DataForML/Data For ProstateX2/Train/DICOM_Train'
patients = os.listdir(data_dir)
#print(patients[6:])
for patient in patients:
  #print("Patient : ",patient)
  label = labels_df.get_value(patient,'ggg')
  region = labels_df.get_value(patient,'zone')
  detail = details_df.get_value(patient,'ijk')
  vspace = details_df.get_value(patient,'VoxelSpacing') #get_value
  #detail = detail.split()
  #print("\tLabel : ",label)
  #print("\tRegion : ",region)
  #print("\tCancer Detail : ",detail)
  #print("\tVspace : ",vspace)
  path = data_dir + "/" + patient
  #b = os.walk(path)
  #print("The Path contains Following :",b)
  a = [x[0] for x in os.walk(path)]
  #print("\t",a[3])
  #s = os.listdir(a[0])
  #print(s)
  #                   a couple great 1-liners from: https://www.kaggle.com/gzuidhof/data-science-bowl-2017/full-preprocessing-tutorial
  slices = [pydicom.read_file(a[3] + '/' + str(s)) for s in os.listdir(a[3])]
  slices.sort(key = lambda x: int(x.ImagePositionPatient[2]))
  #print(len(slices),label)
  #print(slices[0].StudyDate)
  #print(slices[0].StudyDate+str(int(float(slices[0].StudyTime))))
  #print(slices[0])
  patientcase[slices[0].StudyDate+str(int(float(slices[0].StudyTime))).rjust(6, '0')]  = patient
  labelsDict[slices[0].StudyDate+str(int(float(slices[0].StudyTime))).rjust(6, '0')] = label
  regionDict[slices[0].StudyDate+str(int(float(slices[0].StudyTime))).rjust(6, '0')] = region
  CoorDicts[slices[0].StudyDate+str(int(float(slices[0].StudyTime))).rjust(6, '0')] = detail
  voxelSpace[slices[0].StudyDate+str(int(float(slices[0].StudyTime))).rjust(6, '0')] = vspace

print("PatientCase : ",patientcase)
print("Labels Dict : ",labelsDict)
print("Region Dict : ",regionDict)
print("Coordi Dict : ",CoorDicts)
print("Voxel Space : ",voxelSpace)

print("==== Done Creating Dictionaries ====\n")
print("==== Creating Labels,Cases,Regions,Coordinates,Voxel Space Lists For Training ====",end=' ')
Labels= []
for key in sorted(labelsDict.keys()):
    Labels += [labelsDict[key]]
Case = []
for key in sorted(patientcase.keys()):
    Case += [patientcase[key]]
Regions= []
for key in sorted(regionDict.keys()):
    Regions += [regionDict[key]]
Coordinates= []
for key in sorted(CoorDicts.keys()):
    value = CoorDicts[key]
    if type(value) == np.ndarray:
        alist = []
        for i in value:
#             print(np.array([int(j) for j in i.split()]))
            alist += [np.array([int(j) for j in i.split()])]
#         print(alist)
    else:
        alist = [np.array([int(i) for i in value.split()])]
#         print(alist)
    Coordinates += [alist]

Space= []
for key in sorted(voxelSpace.keys()):
    value = voxelSpace[key]
#     print(value)
    if type(value) == np.ndarray:
        alist = []
        for i in value:
#             print(np.array([float(j) for j in i.split(",")]))
            alist += [np.array([float(j) for j in i.split(",")])]
        print(alist)
    else:
        alist = [np.array([float(i) for i in value.split(",")])]
        print(alist)
    Space += [alist]

print("==== Done Creating Lists ====\n")
patients = sorted(patients)


print("===== Creating Stack Of MRI Images for Training =====")
stack = []
for i in patients:
    directory = "C:/Users/user/user/DataForML/Data For ProstateX2/Train/DICOM_Train" + "/" + i
    #print("Patient:",directory)
    dirs = os.listdir(directory)
    midDir = dirs[0]
    #print("Dirs Inside Patient:",midDir)
    dirs = os.listdir(directory+"/"+dirs[0])
    #print("Further Down in Patient : ",dirs)
    dIndex=['tsetra','ADC','BVAL','Ktrans']
    for d in dirs:
      if 'tsetra' in d :
        for furtherDirs in os.listdir(directory+"/"+midDir+"/"+d):
          if '.nii' in os.path.basename(furtherDirs):
            dIndex[0] = midDir + "/" + d + "/" + furtherDirs
      if 'ADC' in d :
        for furtherDirs in os.listdir(directory+"/"+midDir+"/"+d):
          if '.nii' in os.path.basename(furtherDirs):
            dIndex[1] = midDir + "/" + d + "/" + furtherDirs
      if 'BVAL' in d:
        for furtherDirs in os.listdir(directory+"/"+midDir+"/"+d):
          if '.nii' in os.path.basename(furtherDirs):
            dIndex[2] = midDir + "/" + d + "/" + furtherDirs
    for d in os.listdir("C:/Users/user/user/DataForML/Data For ProstateX2/Train/Ktrans_Train" +"/"+i):
      #print(d)
      if '.nii' in os.path.basename(d):
        dIndex[3] = "C:/Users/user/user/DataForML/Data For ProstateX2/Train/Ktrans_Train" +"/"+i+"/"+d

    #print(dIndex)
    t2 = nib.load(directory + "/" + dIndex[0])
    Diff1 = nib.load(directory + "/" + dIndex[1])
    Diff2 = nib.load(directory + "/" + dIndex[2])
    Ktrans = nib.load(dIndex[3])
    #hdr = t2.header
    #print(hdr)
    static = t2.get_data()
    static_grid2world = t2.affine
    moving = Diff1.get_data()
    moving_grid2world = Diff1.affine
    moving2 = Diff2.get_data()
    moving2_grid2world = Diff2.affine
    moving3 = Ktrans.get_data()
    moving3_grid2world = Ktrans.affine
    identity = np.eye(4)

    affine_map = AffineMap(identity,
                           static.shape, static_grid2world,
                           moving.shape, moving_grid2world)
    resampled1 = affine_map.transform(moving)
    affine_map2 = AffineMap(identity,
                           static.shape, static_grid2world,
                           moving2.shape, moving2_grid2world)
    resampled2 = affine_map2.transform(moving2)
    affine_mapk = AffineMap(identity,
                           static.shape, static_grid2world,
                           moving3.shape, moving3_grid2world)
    resampledk = affine_mapk.transform(moving3)

    out= np.stack([static.transpose(2,0,1), resampled1.transpose(2,0,1), resampled2.transpose(2,0,1), resampledk.transpose(2,0,1)], axis=-1)
    #print(out.shape)
    patient = smoothslices(out, 19)
    stack += [patient]

print(" ===== DONE Creating Stacks of MRI IMAGES =====\n")

print(" ===== Cropping and Resizing the Stacked Images [Region of Interest Extraction] ==== ")
#print(len(Labels))
#print(len(Coordinates))
#print(len(Case))
newStack = []
newLabels = []
newCoordinates = []
newCase = []
for i in range(len(stack)):
    print("patient:" + str(i))
    patientseq = stack[i]
    casespace = [j for j in Space[i]]
    casecorr = [j for j in Coordinates[i]]
    print(casecorr)
    for j in range(len(casecorr)):
        print('finding' +str(j))
        lesion = casecorr[j]
        spacing  = casespace[j]
        increments = int((30/spacing[0])/2)
        print(Case[i])
        print(patientseq.shape)
        print(lesion)
        print(spacing)
        print("increments:" + str(increments))
        crop = patientseq[lesion[2]-2:lesion[2]+3, lesion[0]-increments:lesion[0]+increments,lesion[1]-increments:lesion[1]+increments,:]
        print(crop.shape)
        casestack = []
        for c in crop:
            cstack = []
            for s in range(crop.shape[3]):
#                 print(s)
#                 print(c[:,:,s].shape)
                resize = cv2.resize(c[:,:,s], (60, 60))
                cstack += [resize]
            casestack += [np.stack(cstack, axis=-1)]
        print("reshape:--------------------------------------------")
        print(np.array(casestack).shape)
        newStack += [np.array(casestack)]
        newCase += [Case[i]]
        newCoordinates += [casecorr[j]]
        if (len(casecorr) == 1):
            newLabels += [Labels[i]]
            print(Labels[i])
        else:
            newLabels += [Labels[i][j]]
            print(Labels[i][j])

print(" ==== Image Cropping and Resizing DONE ==== \n")

print(" ===== Dumping the PreProcessed Images Using Pickle ==== ")
filename1 = 'ProstateX2-PreProcessed-60x4-Channels'
outfile = open(filename1,'wb')
pickle.dump(np.array(newStack) ,outfile)
pickle.dump(newLabels ,outfile)
pickle.dump(newCoordinates ,outfile)
pickle.dump(newCase, outfile)
# pickle.dump(newRegions ,outfile)
outfile.close()
print(" ===== DUMP in PICKLE Complete =====")

def LoadingPickleFile(filename1=''):
    infile = open(filename1,'rb')
    newStack = pickle.load(infile)
    newLabels = pickle.load(infile)
    newCoordinates = pickle.load(infile)
    newCase = pickle.load(infile)
    infile.close()
    return newStack,newLabels,newCoordinates,newCase
