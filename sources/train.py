#Training Ground for the Project

import pickle
import numpy as np
import pickle
import keras
from keras.models import Model
from keras.layers import Conv3D, Dense, Flatten, MaxPooling3D
from sklearn.metrics import confusion_matrix
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers.core import Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution3D, MaxPooling3D
from keras.engine.input_layer import Input
from keras import optimizers
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score as areauc

print("==== Reading from the Pickle File [created from preProcessing] ====")
infile = open("Data For ProstateX2-PreProcessed-60x4-Channels",'rb')
Images = pickle.load(infile)
Labels = pickle.load(infile)
Coordinates = pickle.load(infile)
Case = pickle.load(infile)
infile.close()
print("==== DONE Reading ====\n")

print(" ==== Creating Training and Validation Sets ====")
train_X = Images[30:, :, :, :, :]
print("Train X : ",len(train_X))
train_y = binaryLabelsreshape[30:]
print("Train Y : ",len(train_y))
val_X = Images[:30, :, :, :, :]
print("Val X : ",len(val_X))
val_y = binaryLabelsreshape[:30]
print("Val Y : ",len(val_y))
print(" ==== DONE ====\n")

trainStats = np.unique(binaryLabels[:], return_counts=True)
#print("Train Stats : ",trainStats)


print("===== Creating 3D CNN =====")
def create_base_network(inputs):
    # Base of the Neural Network
    x = Conv3D(64, kernel_size=(1, 3, 3), activation='relu')(inputs)
    x = Conv3D(64, (1, 3, 3), activation='relu')(x)
    x = Conv3D(128, (1, 3, 3), activation='relu')(x)
    x = Conv3D(128, (1, 3, 3), activation='relu')(x)
    x = MaxPooling3D(pool_size=(1, 2, 2))(x)
    x = Conv3D(256, (3, 3, 3), activation='relu')(x)
    x = Conv3D(512, (3, 3, 3), activation='relu')(x)
    x = Flatten()(x)
    x = Dense(64, activation='relu')(x)

    return x

input_shape = (5, 60, 60, 4)
input1 = Input(shape=input_shape)
input2 = Input(shape=(1,))
mod1 = create_base_network(input1)
x = keras.layers.concatenate([mod1, input2])
output = Dense(2, activation='softmax')(mod1)
model = Model(inputs=[input1], outputs=[output])
sgd = optimizers.SGD(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer= sgd, metrics=['accuracy'])
print(" ===== 3D CNN Model Built and Compiled.Ready For USE ===== \n")

print("\n ===== ** ==== Starting the Training of the 3D CNN Model.This May Take a While.Hang Tight !! ==== ** =====")
MODEL = 'currentCNNmodel.h5'
checkpoint = ModelCheckpoint(MODEL, monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
early = EarlyStopping(monitor='val_loss', min_delta=0, patience=100, verbose=1, mode='auto')
BATCH_SIZE = 32
# Starting Training
hist= model.fit(x=[train_X],y=train_y,epochs = 500,batch_size=BATCH_SIZE,
                validation_data = (val_X, val_y),
                callbacks = [checkpoint, early]
                )
print("\n===== ** === Training Completed.The Best Model is saved as [{}] === ** =====\n".format(MODEL))

choice = (input("Do You Want to Start the Testing on Validation Data ? [For Validation Metrics] \n\tPress:  [Y](Yes) / [N] (No)"))
if choice == 'Y' or 'y':
    import custom_utilities as cst
    import numpy as np
    import matplotlib.pyplot as plt
    model.load_weights(MODEL)
    preds = np.argmax(model.predict([val_X]), axis =-1)
    truths = np.array(binaryLabels[:30])
    cnf_matrix = confusion_matrix(truths, preds)
    accuracy = np.around(accuracy_score(truths, preds),2)
    auc = np.around(areauc(truths, preds), 2)
    prec = np.around(precision_score(truths, preds, average='binary'), 2)
    recall = np.around(recall_score(truths ,preds, average='binary'), 2)
    plot_confusion_matrix(cnf_matrix, classes=['Label1', 'Label2'],
                        title=' Accuracy: ' +str(accuracy)
                        + ', AUC:' + str(auc)
                        + ', Precison:' + str(prec)
                        + ', Recall:' + str(recall)
                     )

print("Exiting.")
