from pyexpat import model
from torch import nn
import torch
from torchvision import models
from PIL import ImageFile
from torchvision import transforms

class UserState():

    label_and_name:dict[str,str]
    model:models.ResNet
    
    def __init__(self):
        self.label_and_name={
            "0": "アメリカンコッカースパニエル",
            "1": "イタリアングレーハウンド",
            "2": "カニンヘンダックスフンド",
            "3": "キャバリア",
            "4": "コーギー",
            "5": "ゴールデンレトリバー",
            "6": "シベリアンハスキー",
            "7": "シーズー",
            "8": "スタンダードプードル",
            "9": "スムースコートチワワ",
            "10": "タイニープードル",
            "11": "チワワ",
            "12": "ティーカッププードル",
            "13": "トイプードル",
            "14": "パグ",
            "15": "パピョン",
            "16": "ビションフリーゼ",
            "17": "フレンチブルドッグ",
            "18": "ブルドッグ",
            "19": "ペキニーズ",
            "20": "ボーダーコリー",
            "21": "ポメラニアン",
            "22": "マルチーズ",
            "23": "ミディアムプードル",
            "24": "ミニチュアシュナウザー",
            "25": "ミニチュアダックスフンド",
            "26": "ヨークシャーテリア",
            "27": "ロングコートチワワ",
            "28": "柴犬",
            "29": "豆柴"
        }

        model = models.resnet18()
        num_ftrs = model.fc.in_features #モデルの最終層の入力サイズ取得
        model.fc = nn.Linear(num_ftrs, 30) #入力そのまま，出力を2まで減らす．

        model.load_state_dict(torch.load("model_weight.pth",map_location={"cuda:0":"cpu"},weights_only=False))
        model.eval()
        self.model=model

        print(self.model)

    def get_dog(self,label:str):
        try:
            return self.label_and_name[label]
        except:
            raise "Dogs not found!!"
    
    def pretend(self,img:ImageFile):

        image_size = 480
        mean = (0.485, 0.456, 0.406)
        std = (0.229, 0.224, 0.225)

        tf=transforms.Compose([
            transforms.Resize(image_size),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize(mean, std)
        ])

        with torch.no_grad():
            self.model.eval()
            img_tensor=tf(img).unsqueeze(0)
            out=self.model(img_tensor)
            pred=torch.argmax(out,1)
        
        return self.label_and_name[str(pred.item())]