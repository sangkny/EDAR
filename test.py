import argparse
import os
import io
import torch
import torch.backends.cudnn as cudnn
from torchvision import transforms
import PIL.Image as pil_image
<<<<<<< HEAD

from edar import EDAR
=======
from ar_0hyenet import AR_0hyeNet
>>>>>>> a10f627eccd54a352dddaab534372689f5d7e4a8

cudnn.benchmark = True
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights_path', type=str, required=True)
    parser.add_argument('--image_path', type=str, required=True)
    parser.add_argument('--outputs_dir', type=str, required=True)
    parser.add_argument('--jpeg_quality', type=int, default=40)
    opt = parser.parse_args()

    if not os.path.exists(opt.outputs_dir):
        os.makedirs(opt.outputs_dir)

    model = AR_0hyeNet()

    state_dict = model.state_dict()
    for n, p in torch.load(opt.weights_path, map_location=lambda storage, loc: storage).items():
        if n in state_dict.keys():
            state_dict[n].copy_(p)
        else:
            raise KeyError(n)

    model = model.to(device)
    model.eval()

    filename = os.path.basename(opt.image_path).split('.')[0]

    input = pil_image.open(opt.image_path).convert('RGB')

    buffer = io.BytesIO()
    input.save(buffer, format='jpeg', quality=opt.jpeg_quality)
    input = pil_image.open(buffer)
    input.save(os.path.join(opt.outputs_dir, '{}_jpeg_q{}.png'.format(filename, opt.jpeg_quality)))

    input = transforms.ToTensor()(input).unsqueeze(0).to(device)

    with torch.no_grad():
        pred = model(input)[-1]

    pred = pred.mul_(255.0).clamp_(0.0, 255.0).squeeze(0).permute(1, 2, 0).byte().cpu().numpy()
    output = pil_image.fromarray(pred, mode='RGB')
<<<<<<< HEAD
    output.save(os.path.join(opt.outputs_dir, '{}_{}.png'.format(filename, "AR_RCAN")))
=======
    output.save(os.path.join(opt.outputs_dir, '{}_{}.png'.format(filename, "AR_0hyeNet")))
>>>>>>> a10f627eccd54a352dddaab534372689f5d7e4a8
