import numpy as np
import matplotlib
matplotlib.use('Agg')

import torch
import cv2

from models.net import SPPNet

test_image_path = '/home/ubuntu/data/Segmentation/pytorch-segmentation/test1.jpg'

print('Loading model...')

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = SPPNet(output_channels=19).to(device)
model_path = '../model/cityscapes_deeplab_v3_plus/model.pth'
param = torch.load(model_path)
model.load_state_dict(param)
del param

batch_size = 1

# Notify layers that we are in eval mode (for batchnorm, dropout)
model.eval()
# Deactivate autograd engine to reduce memory usage (no need backprop when inferring)
with torch.no_grad():
    print('Loading input image...')
    img = cv2.imread(test_image_path, cv2.IMREAD_COLOR)

    print('Displaying input image...')

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    print('Predicting...')

    img = img.transpose(2, 0, 1)
    img_tensor = torch.tensor([img])
    img_tensor = img_tensor.float()
    print('A'+str(type(img_tensor)))
    print(img_tensor.size())

    # Send to CPU or GPU depending on the hardware found
    img_tensor = img_tensor.to(device)

    # Generate predictions
    preds = model.tta(img_tensor, net_type='deeplab')
    preds = preds.argmax(dim=1)

    print(preds.size())

    preds_np = preds.detach().cpu().numpy()

    print(type(preds_np))

