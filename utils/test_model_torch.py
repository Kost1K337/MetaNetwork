import torch
import numpy as np
import pyarrow.dataset as ds
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import pickle


if __name__ == '__main__':

    scaler = MinMaxScaler()

    min_values = np.loadtxt('min_values.txt')
    max_values = np.loadtxt('max_values.txt')

    scaler.fit([min_values, max_values])

    with open('scaler.pickle', 'wb') as pfile:
        pickle.dump(scaler, pfile)


    device = torch.device('cuda' if not torch.cuda.is_available() else 'cpu')
    model = torch.jit.load("model.pth")
    model.to(device)

    dataset = ds.dataset('vfp_parts_small', format='parquet')

    gpu_size = 98304
    data = dataset.to_batches(batch_size=gpu_size)

    mape = 0

    r2_arr = []

    already_read = 0

    batch = next(data)
    model.eval()
    chunk = batch.to_pandas()
    scaled = scaler.transform(chunk.values)
    x = scaled[:, 1:]
    
    X_batch = torch.tensor(x, device=device, dtype=torch.float)
    predicted = model(X_batch).detach().numpy()
    predicted_backscaled = predicted * (max_values[0] - min_values[0]) + min_values[0]
    
    mape = mean_absolute_percentage_error(chunk.values[:, 0], predicted_backscaled)
    r2 = r2_score(chunk.values[:, 0], predicted_backscaled)

    print(f'MAPE: {mape} R2: {r2}')

