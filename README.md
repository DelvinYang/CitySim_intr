# CitySim_intr

This repository contains scripts for converting trajectory data from the **UCF-SST-CitySim1** dataset into tensors suitable for machine learning models.

## Dependencies

The following Python packages are required:

- `torch`
- `numpy`
- `pandas`
- `loguru`
- `tqdm`

Install them with pip:

```bash
pip install torch numpy pandas loguru tqdm
```

## Data Preparation

Download the trajectory CSV files from the [UCF-SST-CitySim1 dataset](https://github.com/UCF-SST-Lab/UCF-SST-CitySim1-Dataset/wiki) and organise them as:

```
<DATA_PATH>/IntersectionA/Trajectories/IntersectionA-01.csv
```

The dataset records one row per vehicle per frame. Important fields are described in `AGENTS.md`:

- `frameNum`: video frame number (30 fps)
- `carId`: unique vehicle identifier
- `carCenterX`, `carCenterY`: pixel coordinates of the bounding box centre
- `headX`/`headY`, `tailX`/`tailY`: front and rear centre points
- `boundingBox1X` ~ `boundingBox4Y`: pixel coordinates of the four corners
- `speed`: recorded vehicle speed

Refer to `AGENTS.md` for the complete list of fields and units.

## Running the Example

`main.py` converts the CSV data into sequences and saves them as `sequence_tensor_dataset.pt`.
Specify the data location via command-line arguments:

```bash
python main.py --data-path <DATA_PATH> --location-name IntersectionA --prefix-number 01
```

Processing progress is displayed with `tqdm` and the resulting tensor dataset is saved in the project root.

