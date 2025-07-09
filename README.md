[Click aqui para leer el documento en Español](es_README.md)  
[Clickez ici pour lire le document traduit au français](fr_README.md)

# GBP_Simu - Detection on a simulation of a board's good or bad positionning on the main production line

### Usage
### If you want to train your own model with the data
1. Clone the repository  
2. Unzip data.zip and load it in the project's root (where it already is). This divides the 4 situations/positions the model can detect.  
3. Download all of the releases of this Git ([Simu_Video](https://github.com/IsmaTIBU/GBP_Simu/releases/tag/Simu_Video)) and load it on the project's root, as we did with the folder 'data'  
4. Execute 'video_mask.py' to generate a video of the production line applying it a mask so the model can focus on the 2 main positions and less data is required to train it, it will take some time. The result will be loaded in Output/output_masked_video.mp4.  
5. Execute 'Training.py'. It will train the model, ideally you should find val_loss and loss finish on a rather same value and accuracy and val_accuracy would have a rather high note (from 0-1).

6. Execute 'Model_test.py'. Here we label the masked video with squares that change color depending on the position of the board, in other words, depending on what the model detects.

#### If you wish to use this project for a personal simulation you should record a video, use it in 'videoToPhoto.py' as input, which will divide the video in all of its frames and save them in 'data', and then put the different positions in their respective folder. You will also have to change the masks configurations in 'video_mask.py' and the labeling in 'Model_test.py'.   

### If you wish only to visualize the results with the current trained model  
1. Clone the repository
2. Unzip data.zip and load it in the project's root (where it already is). This divides the 4 situations/positions the model can detect.
3. Download all of the releases of this Git ([Simu_Video](https://github.com/IsmaTIBU/GBP_Simu/releases/tag/Simu_Video) & [PositionDetection_Model](https://github.com/IsmaTIBU/GBP_Simu/releases/tag/PosiotionDetection_Model)) and load them on the project's root, as we did with the folder 'data'  
4. Execute 'video_mask.py' to generate a video of the production line applying it a mask so the model can focus on the 2 main positions and less data is required to train it, it will take some time. The result will be loaded in Output/output_masked_video.mp4.  
5. Execute 'Model_test.py'. Here we label the masked video with squares that change color depending on the position of the board, in other words, depending on what the model detects.

