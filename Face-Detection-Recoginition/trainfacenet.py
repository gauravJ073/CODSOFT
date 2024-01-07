# pylint: disable=missing-module-docstring
# pylint: disable=consider-using-f-string
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=import-error

import os
from facenet_pytorch import InceptionResnetV1, fixed_image_standardization, training
import torch
from torch.utils.data import DataLoader, SubsetRandomSampler
from torch import optim
from torch.optim.lr_scheduler import MultiStepLR
from torchvision import datasets, transforms
import numpy as np


device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))
class TrainFacenet():
    def __init__(self):
        self.data_dir = 'Face-Detection-Recoginition\\tmp\\'
        self.batch_size = 32
        self.epochs = 8
        self.workers = 0 if os.name == 'nt' else 8


        trans = transforms.Compose([
           np.float32,
           transforms.ToTensor(),
           transforms.Resize(160,160,3),
           fixed_image_standardization
       ])

        self.dataset = datasets.ImageFolder(self.data_dir, transform=trans)
        self.img_inds = np.arange(len(self.dataset))
        # print(self.img_inds)
        np.random.shuffle(self.img_inds)
        self.train_inds = self.img_inds[:int(0.8 * len(self.img_inds))]
        self.val_inds = self.img_inds[int(0.8 * len(self.img_inds)):]
        print(SubsetRandomSampler(self.train_inds))

        self.train_loader = DataLoader(
           self.dataset,
           num_workers=self.workers,
           batch_size=self.batch_size,
           sampler=SubsetRandomSampler(self.train_inds)
        )
        self.val_loader = DataLoader(
           self.dataset,
           num_workers=self.workers,
           batch_size=self.batch_size,
           sampler=SubsetRandomSampler(self.val_inds)
        )

        self.resnet = InceptionResnetV1(
          classify=True,
          pretrained='vggface2',
          num_classes=len(self.dataset.class_to_idx)
        ).to(device)


        self.optimizer = optim.Adam(self.resnet.parameters(), lr=0.001)
        self.scheduler = MultiStepLR(self.optimizer, [5, 10])


        self.loss_fn = torch.nn.CrossEntropyLoss()
        self.metrics = {
          'fps': training.BatchTimer(),
          'acc': training.accuracy
        }

# writer = SummaryWriter()
# writer.iteration, writer.interval = 0, 10
    def TrainModel(self):
        print('\n\nInitial')
        print('-' * 10)
        self.resnet.eval()
        training.pass_epoch(
            self.resnet, self.loss_fn, self.val_loader,
            batch_metrics=self.metrics, show_running=True, device=device
        )

        for epoch in range(self.epochs):
            print('\nEpoch {}/{}'.format(epoch + 1, self.epochs))
            print('-' * 10)

            self.resnet.train()
            training.pass_epoch(
                self.resnet, self.loss_fn, self.train_loader, self.optimizer, self.scheduler,
                batch_metrics=self.metrics, show_running=True, device=device
            )

            self.resnet.eval()
            training.pass_epoch(
                self.resnet, self.loss_fn, self.val_loader,
                batch_metrics=self.metrics, show_running=True, device=device
            )
        return self.resnet

trainfc=TrainFacenet()
resnet=trainfc.TrainModel()
