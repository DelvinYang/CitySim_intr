import os

import numpy as np
from loguru import logger

from common import *
import pandas as pd


class DataReaderCitySim(object):
    def __init__(self, location_name, prefix_number, data_path):
        self.location_name = location_name
        self.prefix_number = prefix_number
        self.data_path = data_path
        self.csv_tracks_path = self.generate_path()
        self.tracks, self.id_list = self.read_tracks_csv()
        logger.info(f"read data done, total tracks: {len(self.tracks)}")

    def generate_path(self):
        # 构建文件名：{location_name}-{prefix_number}.csv
        filename = f"{self.location_name}-{self.prefix_number}.csv"

        # 构建完整路径：data_path/location_name/Trajectories/...
        full_path = os.path.join(
            self.data_path,
            self.location_name,
            "Trajectories",
            filename
        )

        return str(full_path)

    def read_tracks_csv(self):
        # Read the csv file, convert it into a useful data structure
        df = pd.read_csv(self.csv_tracks_path)
        grouped = df.groupby([TRACK_ID], sort=False)

        tracks = []
        id_list = set()
        for group_id, rows in grouped:
            speed_values = rows[SPEED].values

            # 如果 speed 全为 0 或 NaN → 跳过轨迹
            if np.all(np.nan_to_num(speed_values) == 0):
                logger.info(f"Track {group_id} skipped: all speed values are 0 (len={len(speed_values)})")
                continue

            # =================== 尺寸 =====================

            # 前角对：1 和 4
            dx14 = (rows['boundingBox1Xft'].values - rows['boundingBox4Xft'].values) * FT_TO_M
            dy14 = (rows['boundingBox1Yft'].values - rows['boundingBox4Yft'].values) * FT_TO_M
            width14 = np.sqrt(dx14 ** 2 + dy14 ** 2)

            # 后角对：2 和 3
            dx23 = (rows['boundingBox2Xft'].values - rows['boundingBox3Xft'].values) * FT_TO_M
            dy23 = (rows['boundingBox2Yft'].values - rows['boundingBox3Yft'].values) * FT_TO_M
            width23 = np.sqrt(dx23 ** 2 + dy23 ** 2)

            width = 0.5 * (width14 + width23)

            # 右边对角：1 和 2
            dx12 = (rows['boundingBox1Xft'].values - rows['boundingBox2Xft'].values) * FT_TO_M
            dy12 = (rows['boundingBox1Yft'].values - rows['boundingBox2Yft'].values) * FT_TO_M
            length12 = np.sqrt(dx12 ** 2 + dy12 ** 2)

            # 左边对角：4 和 3
            dx43 = (rows['boundingBox4Xft'].values - rows['boundingBox3Xft'].values) * FT_TO_M
            dy43 = (rows['boundingBox4Yft'].values - rows['boundingBox3Yft'].values) * FT_TO_M
            length43 = np.sqrt(dx43 ** 2 + dy43 ** 2)

            length = 0.5 * (length12 + length43)

            # =================== 位置 =====================
            x_pos = rows['carCenterXft'].values * FT_TO_M
            y_pos = rows['carCenterYft'].values * FT_TO_M

            bounding_boxes = np.stack([x_pos, y_pos, length, width], axis=1)

            dt = 1 / 30.0  # 30 Hz sampling frequency

            def deriv_5point(arr):
                """First derivative using a 5-point stencil."""
                n = len(arr)
                d = np.zeros_like(arr, dtype=float)
                if n >= 5:
                    d[2:-2] = (
                        -arr[:-4] + 8 * arr[1:-3] - 8 * arr[3:-1] + arr[4:]
                    ) / (12 * dt)
                    d[0] = (arr[1] - arr[0]) / dt
                    d[1] = (arr[2] - arr[0]) / (2 * dt)
                    d[-2] = (arr[-1] - arr[-3]) / (2 * dt)
                    d[-1] = (arr[-1] - arr[-2]) / dt
                elif n > 1:
                    d[1:] = np.diff(arr) / dt
                    d[0] = d[1]
                return d

            def second_deriv_5point(arr):
                """Second derivative using a 5-point stencil."""
                n = len(arr)
                d2 = np.zeros_like(arr, dtype=float)
                if n >= 5:
                    d2[2:-2] = (
                        -arr[:-4]
                        + 16 * arr[1:-3]
                        - 30 * arr[2:-2]
                        + 16 * arr[3:-1]
                        - arr[4:]
                    ) / (12 * dt ** 2)
                    d2[0] = (arr[0] - 2 * arr[1] + arr[2]) / (dt ** 2)
                    d2[1] = (arr[0] - 2 * arr[1] + arr[2]) / (dt ** 2)
                    d2[-2] = (arr[-3] - 2 * arr[-2] + arr[-1]) / (dt ** 2)
                    d2[-1] = (arr[-3] - 2 * arr[-2] + arr[-1]) / (dt ** 2)
                elif n > 2:
                    d2[1:-1] = (arr[2:] - 2 * arr[1:-1] + arr[:-2]) / (dt ** 2)
                    d2[0] = d2[1]
                    d2[-1] = d2[-2]
                return d2

            # 5-point derivative to smooth velocity and acceleration
            x_velocity = deriv_5point(x_pos)
            y_velocity = deriv_5point(y_pos)

            x_acceleration = second_deriv_5point(x_pos)
            y_acceleration = second_deriv_5point(y_pos)

            speed_computed = np.sqrt(x_velocity ** 2 + y_velocity ** 2)  # 单位 m/s
            # ========== 原始 speed 转为 m/s ==========
            speed_values = rows[SPEED].values * MPH_TO_MPS  # mph → m/s
            # ========= 判断是否异常（默认允许最大误差 ±3m/s）=========
            speed_diff = np.abs(speed_computed - speed_values)
            if np.mean(speed_diff) > 0.5:
                logger.warning(
                    f"Track {group_id} skipped: computed speed differs too much from recorded speed (mean_diff = {np.mean(speed_diff):.2f} m/s)")
                continue

            course_rad = np.deg2rad(rows[COURSE].values)

            # Frenet 坐标轴：前向 unit 向量 (lon) 和横向 unit 向量 (lat)
            lon_unit = np.stack([np.cos(course_rad), np.sin(course_rad)], axis=1)  # 朝向方向
            lat_unit = np.stack([-np.sin(course_rad), np.cos(course_rad)], axis=1)  # 横向方向（右手系）

            velocity_vec = np.stack([x_velocity, y_velocity], axis=1)
            acceleration_vec = np.stack([x_acceleration, y_acceleration], axis=1)

            # 投影为 Frenet 坐标分量
            v_lon = np.sum(velocity_vec * lon_unit, axis=1)
            v_lat = np.sum(velocity_vec * lat_unit, axis=1)

            a_lon = np.sum(acceleration_vec * lon_unit, axis=1)
            a_lat = np.sum(acceleration_vec * lat_unit, axis=1)

            track_data = {TRACK_ID: np.int64(group_id),
                             # for compatibility, int would be more space efficient
                             FRAME: rows[FRAME].values,
                             BBOX: bounding_boxes,
                          X_VELOCITY: x_velocity,
                          Y_VELOCITY: y_velocity,
                          X_ACCELERATION: x_acceleration,
                          Y_ACCELERATION: y_acceleration,
                          LON_VELOCITY: v_lon,
                          LAT_VELOCITY: v_lat,
                          LON_ACCELERATION: a_lon,
                          LAT_ACCELERATION: a_lat,
                                     }
            tracks.append(track_data)
            id_ = np.int64(group_id)[0]
            id_list.add(id_)
        return tracks, id_list
