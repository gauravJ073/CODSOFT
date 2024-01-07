# pylint: disable=missing-function-docstring

# pylint: disable=line-too-long
# pylint: disable=too-many-locals
# pylint: disable=missing-module-docstring
# pylint: disable=bare-except
# pylint: disable=import-error
# pylint: disable=too-few-public-methods



import pickle
import cv2
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
from sklearn.preprocessing import LabelEncoder


class FaceDetector():
    """
    Face detector class
    """
    def __init__(self):
        self.mtcnn = MTCNN(image_size=240, margin=0, keep_all=True, min_face_size=40)# keep_all=True
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()#loading facenet pretrained for getting embeddings

        self.encoder=LabelEncoder()
        self.encoder.classes_=np.load("Face-Detection-Recognition/classifier/classes.npy")#loading the saved encoder
        print(self.encoder.classes_)
        with open('Face-Detection-Recognition/classifier/svm_classifier.pkl', 'rb') as loaded_model:#loading the saved model
            self.classifier=pickle.load(loaded_model)



    def run(self):
        cap = cv2.VideoCapture(0)#capturing video from camera

        while True:
            _, frame = cap.read() #reading frames from the video
            try:
                # detect face box
                img = Image.fromarray(frame)
                img_cropped_list, prob_list = self.mtcnn(img, return_prob=True)
                boxes = self.mtcnn.detect(img)

                for i, prob in enumerate(prob_list):
                    if prob>0.80:
                        emb = self.resnet(img_cropped_list[i].unsqueeze(0)).detach()

                        prediction=self.classifier.predict(emb)
                        name=self.encoder.inverse_transform(prediction)[0]

                        box = boxes[i]

                        frame = cv2.rectangle(frame, (int(box[i][0]),int(box[i][1])) , (int(box[i][2]),int(box[i][3])), (255,0,0), 2)
                        frame = cv2.putText(frame, name, (int(box[i][0]),int(box[i][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),1, cv2.LINE_AA)


            except:
                pass
            # Show the frame
            cv2.imshow('Face Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
# Run the app
fcd = FaceDetector()
fcd.run()
