# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=import-error
# pylint: disable=missing-module-docstring
# pylint: disable=consider-using-f-string
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring

# importing libraries

import os
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torchvision import datasets
from torch.utils.data import DataLoader


#creating embeddings to train a classifier

class CreateEmbedding():
    def __init__(self):
        self.mtcnn0 = MTCNN(image_size=240, margin=0, keep_all=False, min_face_size=40) # keep_all=False
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()
    def run(self):
        #getting the dataset
        dataset = datasets.ImageFolder('Face-Detection-Recognition/data/') # photos folder path
        idx_to_class = {i:c for c,i in dataset.class_to_idx.items()} # accessing names of peoples from folder names

        def collate_fn(x):
            return x[0]

        #using torch dataloader object to load data later
        loader = DataLoader(dataset, collate_fn=collate_fn)

        name_list = [] # list of names corrospoing to cropped photos
        embedding_list = [] # list of embeding matrix after conversion from cropped faces to embedding matrix using resnet
        savepath="Face-Detection-Recognition/embeddings"
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        i=0
        for img, idx in loader:
            #there are 862 images in "Face-Detection-Recoginition/data/Gaurav/" directory,
            # hence we are loading a total of 1724 images to keep the number of images in "Gaurav" and "Not Gaurav" classes same.
            if i>=1724:
                break
            #getting face and probablity of detected face being a face
            face, prob = self.mtcnn0(img, return_prob=True)
            if face is not None and prob>0.60:
                #getting embeddings using pretrained resnet
                emb = self.resnet(face.unsqueeze(0))
                #saving embeddings and coresponding name of classes (Gaurav / Not Gaurav)
                embedding_list.append(emb.detach())
                name_list.append(idx_to_class[idx])
                i+=1

        # saving the embeddings on disk to train the classifier
        data = [embedding_list, name_list]
        torch.save(data, f'{savepath}/data.pt')

ce=CreateEmbedding()
ce.run()
