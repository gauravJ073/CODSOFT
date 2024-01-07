# Face Detection and recoginition

The task of Face detection and recognition includes 4 main subtasks:
1. Training a model to classify faces
   1.1 Use face detector to get faces from images in dataset
   1.2 Use pretrained neural network to get embeddings(or face features)
   1.3 Use the embeddings to train a classifier (like a SVC)
2. Performing Face Detection 
3. Generating embeddings using the same pretrained neural netowrk
4. Using pretrained classifier to classify the images


For this project, MTCNN was used for face detection and pretrained FaceNet model for getting face embeddings.
Images in data/Not_Gaurav/ are from the follwoing dataset: [https://www.kaggle.com/datasets/ashwingupta3012/human-faces]