from torchvision import datasets
import torchvision.transforms as transforms

dir_ = '/content/drive/MyDrive/models/CartoonGan-tensorflow/datasets/popeye'
dataset_ = datasets.ImageFolder(dir_, transform=transforms.Compose(
                                        [transforms.Resize(opt.img_size), transforms.CenterCrop(opt.img_size),transforms.ToTensor(), transforms.Normalize([0.5], [0.5])]
                                      ),)
dataloader = torch.utils.data.DataLoader(dataset_,
                                        batch_size=opt.batch_size,
                                        shuffle=True,)