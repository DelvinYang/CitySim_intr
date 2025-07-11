from typing import List

import torch
from loguru import logger
from tqdm import tqdm

from common import State
from read_data_CitySim import DataReaderCitySim
from scenariocitysim import ScenarioCitySim, Vehicle

logger.info("start main")
location_name, prefix_number, data_path = 'IntersectionA', '01', '/Users/delvin/Downloads/Citysim'
past_frames_needed = 12

data_reader = DataReaderCitySim(location_name, prefix_number, data_path)
scenario = ScenarioCitySim(data_reader)

all_sequence_samples = []

for ego_id in tqdm(data_reader.id_list, desc="Processing ego_ids"):
    ego_veh: Vehicle = scenario.find_vehicle_by_id(ego_id)

    start_frame = ego_veh.initial_frame
    end_frame = ego_veh.final_frame

    total_available = end_frame - start_frame

    if total_available < past_frames_needed + 1:
        continue  # 不足 12+1 帧，跳过该车

    # === 顺序采样：采 12 帧，跳过 12 帧
    step = past_frames_needed + 12
    available_start_indices = list(range(start_frame, end_frame - past_frames_needed, step))

    # 过滤掉可能越界的起始帧
    available_start_indices = [
        idx for idx in available_start_indices
        if idx + past_frames_needed <= end_frame
    ]

    # logger.info(f"ego_id {ego_id}: usable sequence start frames: {available_start_indices}")

    for idx in available_start_indices:
        frame_feature_list = []
        valid = True

        for offset in range(past_frames_needed):
            frame_num = idx + offset
            try:
                ego_state: State = scenario.find_vehicle_state(frame_num, ego_id)
                svs_state: List[State] = scenario.find_svs_state(frame_num, ego_id)

                # === ego 特征 ===
                ego_feature = torch.tensor(
                    ego_state.lon + ego_state.lat,
                    dtype=torch.float
                )  # [4]

                # === 周围车特征 ===
                ego_pos = torch.tensor([ego_state.x[0], ego_state.y[0]], dtype=torch.float)
                ego_heading = ego_state.course_rad

                # Neighbour selection based purely on relative position to the ego
                # car. We rotate all neighbours into the ego frame and then pick
                # the closest car in each of the eight sectors around the ego.
                cos_h = torch.cos(ego_heading)
                sin_h = torch.sin(ego_heading)
                dir_best = {}

                for sv in svs_state:
                    sv_pos = torch.tensor([sv.x[0], sv.y[0]], dtype=torch.float)
                    delta = sv_pos - ego_pos

                    # transform into ego's coordinate system
                    local_x = cos_h * delta[0] + sin_h * delta[1]
                    local_y = -sin_h * delta[0] + cos_h * delta[1]
                    dist = torch.norm(delta, p=2).item()

                    angle = torch.atan2(local_y, local_x).item()
                    if -0.39269908 <= angle < 0.39269908:
                        idx = 0  # front
                    elif 0.39269908 <= angle < 1.17809725:
                        idx = 1  # front-right
                    elif 1.17809725 <= angle < 1.9634954:
                        idx = 2  # right
                    elif 1.9634954 <= angle < 2.74889357:
                        idx = 3  # rear-right
                    elif angle >= 2.74889357 or angle < -2.74889357:
                        idx = 4  # rear
                    elif -2.74889357 <= angle < -1.9634954:
                        idx = 5  # rear-left
                    elif -1.9634954 <= angle < -1.17809725:
                        idx = 6  # left
                    else:
                        idx = 7  # front-left

                    sv_feat = torch.tensor(sv.lon + sv.lat, dtype=torch.float)
                    prev = dir_best.get(idx)
                    if prev is None or dist < prev[0]:
                        dir_best[idx] = (dist, sv_feat)

                sv_features = []
                for d in range(8):
                    if d in dir_best:
                        sv_features.append(dir_best[d][1])
                    else:
                        sv_features.append(torch.zeros(4))

                frame_feature = torch.stack([ego_feature] + sv_features, dim=0)  # [9, 4]
                frame_feature_list.append(frame_feature)

            except Exception as e:
                logger.warning(f"skip sample at frame {frame_num} for ego {ego_id} due to {e}")
                valid = False
                break

        if valid:
            try:
                target_state = scenario.find_vehicle_state(idx + past_frames_needed, ego_id)
                label = torch.tensor([target_state.x[2], target_state.y[2]], dtype=torch.float)

                sequence_tensor = torch.stack(frame_feature_list, dim=0)  # [T, 9, 4]
                all_sequence_samples.append((sequence_tensor, label))
            except Exception as e:
                logger.warning(f"skip label for ego {ego_id} due to {e}")
                continue

logger.info(f"Total samples collected: {len(all_sequence_samples)}")
save_path = "./sequence_tensor_dataset.pt"
torch.save(all_sequence_samples, save_path)

logger.info(f"Saved dataset with {len(all_sequence_samples)} samples to {save_path}")
