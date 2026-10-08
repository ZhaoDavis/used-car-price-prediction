import numpy as np
import pandas as pd
import lightning as L
import torch
from torch import nn   
from torch import optim
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, TargetEncoder, StandardScaler

class Model(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.nn = nn.Sequential(
            nn.Linear(64, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64,1)
        )
        self.loss_fn = nn.SmoothL1Loss()

    def forward(self, batch):
        x = self.nn(batch)
        return x
    
    def training_step(self, batch):
        x, y = batch
        y_pred = self.forward(x)
        loss = self.loss_fn(y_pred, y)
        return loss

    def validation_step(self, batch):
        x, y = batch
        y_pred = self.forward(x)
        loss = self.loss_fn(y_pred, y)
        self.log("val_loss", loss, on_step=False, on_epoch=True)
        return loss    
    
    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=0.0003)
        return optimizer

def predict(miles, year, enginesize, make, model, body, drivetrain, transmission, fuel):
    input_df = pd.DataFrame([{
        "miles": miles,
        "year": year,
        "engine_size": enginesize,
        "make": make,
        "model": model,
        "body_type": body,
        "drivetrain": drivetrain,
        "transmission": transmission,
        "fuel_type": fuel,
    }])
    print(input_df)
    preprocessors = joblib.load("./model/preprocessors.joblib")

    input_df_processed = preprocessors.transform(input_df)

    pd.set_option("display.max_columns", 340)
    input_df_processed = input_df_processed.astype(float)

    checkpoint_model = Model.load_from_checkpoint("./model/model.ckpt")
    checkpoint_model.to(torch.device('cpu'))
    checkpoint_model.eval()

    user_tensor = torch.tensor(input_df_processed, dtype = torch.float32)
    user_tensor.dtype

    with torch.no_grad():
        pred = checkpoint_model(user_tensor)

    pred = pred.detach().cpu()
    predicted_val = np.exp(pred)

    return round(float(predicted_val), 2)

print(predict(17631, 2020, 2, "Ford", "Edge", "SUV", "4WD", "Automatic", "Unleaded"))
