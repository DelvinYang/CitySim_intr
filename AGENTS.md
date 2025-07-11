# UCF-SST-CitySim1 Trajectory 数据说明

UCF-SST-CitySim1 数据集包含由无人机拍摄的车辆轨迹数据，视频帧率为 **30 fps**。轨迹数据中，每一行表示某一辆车在某一帧的状态，并提供了带有旋转信息的车辆包围盒。
坐标系的原点在图像左上角角点, x向下 y 向右

---

## 📌 Trajectory 数据字段说明

| 名称 | 描述 | 单位 |
|------|------|------|
| `frameNum` | 视频帧编号（30fps） | - |
| `carId` | 车辆唯一标识（贯穿整个视频） | - |
| `carCenterX` | 车辆包围盒中心的 x 像素坐标 | Pixel |
| `carCenterY` | 车辆包围盒中心的 y 像素坐标 | Pixel |
| `headX` | 包围盒前中心点的 x 像素坐标 | Pixel |
| `headY` | 包围盒前中心点的 y 像素坐标 | Pixel |
| `tailX` | 包围盒后中心点的 x 像素坐标 | Pixel |
| `tailY` | 包围盒后中心点的 y 像素坐标 | Pixel |
| `boundingBox1X` ~ `boundingBox4Y` | 包围盒四个顶点的像素坐标（x, y 各四个） | Pixel |
| `carCenterXft` ~ `carCenterYft` | 包围盒中心点的真实坐标（英尺） | Feet |
| `headXft` ~ `tailYft` | 包围盒前/后中心点的真实坐标（英尺） | Feet |
| `boundingBox1Xft` ~ `boundingBox4Yft` | 四个顶点的真实坐标（英尺） | Feet |
| `carCenterLat` ~ `carCenterLon` | 包围盒中心点的全球经纬度 | Degrees |
| `headLat` ~ `tailLon` | 前/后中心点的全球经纬度 | Degrees |
| `boundingBox1Lat` ~ `boundingBox4Lon` | 四个顶点的全球经纬度 | Degrees |
| `speed` | 车辆速度 | Miles per Hour |
| `heading` | 相对地理北方向的航向角 | Degrees |
| `course` | 相对于图像 X 轴的航向角 | Degrees |
| `laneId` | 所在车道编号（与车道图配合使用） | - |

> 注：经纬度字段（带 `Lat`/`Lon` 后缀）仅在 **美国地区数据** 中提供。

---

## 🚘 Vehicle Point Features（车辆关键点）

数据集中车辆关键点如下图所示（未附图时可结合描述理解）：

- **包围盒 Point 1**：车辆右前角（Front Right）
- **包围盒 Point 2**：车辆右后角（Rear Right）
- **包围盒 Point 3**：车辆左后角（Rear Left）
- **包围盒 Point 4**：车辆左前角（Front Left）
- **headX/Y**：车辆前方中心点坐标
- **tailX/Y**：车辆后方中心点坐标
- **carCenterX/Y**：车辆中心点坐标

---

## 📁 数据源

详细文档和数据下载请参考：[UCF-SST-CitySim1 GitHub Wiki](https://github.com/UCF-SST-Lab/UCF-SST-CitySim1-Dataset/wiki)
