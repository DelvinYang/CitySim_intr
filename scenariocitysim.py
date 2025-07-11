from loguru import logger

from read_data_CitySim import DataReaderCitySim
from common import *

class ScenarioCitySim(object):
    def __init__(self, data_reader: DataReaderCitySim):
        self.data_reader = data_reader
        self.vehicles = self.set_vehicles()

    def set_vehicles(self):
        vehicles_dict = {}
        for track in self.data_reader.tracks:
            track_id = track[TRACK_ID][0]
            vehicles_dict[track_id] = Vehicle(track)

        return vehicles_dict

    def find_vehicle_by_id(self, vehicle_id):
        vehicle = self.vehicles[vehicle_id]
        return vehicle

    def set_reference_path(self, ego_id):
        reference_path = []
        ego_vehicle = self.find_vehicle_by_id(ego_id)
        for sublist in ego_vehicle.track[BBOX]:
            x, y, w, h = sublist
            center = (x + 0.5 * w, y + 0.5 * h)
            reference_path.append(center)

        return reference_path

    def find_vehicle_state(self, frame_num, vehicle_id):
        vehicle = self.vehicles[vehicle_id]
        if vehicle.initial_frame <= frame_num <= vehicle.final_frame:
            index = frame_num - vehicle.initial_frame
            x = vehicle.track[BBOX][index][0]
            y = vehicle.track[BBOX][index][1]
            x_velocity = vehicle.track[X_VELOCITY][index]
            y_velocity = vehicle.track[Y_VELOCITY][index]
            x_acceleration = vehicle.track[X_ACCELERATION][index]
            y_acceleration = vehicle.track[Y_ACCELERATION][index]

            lon_velocity = vehicle.track[LON_VELOCITY][index]
            lat_velocity = vehicle.track[LAT_VELOCITY][index]
            lon_acceleration = vehicle.track[LON_ACCELERATION][index]
            lat_acceleration = vehicle.track[LAT_ACCELERATION][index]
            course_rad = vehicle.track[COURSE_RAD][index]

            x_value = [x, x_velocity, x_acceleration]
            y_value = [y, y_velocity, y_acceleration]
            lon_value = [lon_velocity, lon_acceleration]
            lat_value = [lat_velocity, lat_acceleration]

            width = vehicle.track[BBOX][index][2]
            height = vehicle.track[BBOX][index][3]


            state_f = State(vehicle_id, x_value, y_value, lon_value, lat_value, width, height, course_rad)
            return state_f
        else:
            return None

    def find_svs_state(self, frame_num, vehicle_id):
        svs_state = []
        for vehicle in self.vehicles.values():
            if vehicle.vehicle_id != vehicle_id:
                try:
                    state = self.find_vehicle_state(frame_num=frame_num, vehicle_id=vehicle.vehicle_id)
                except Exception as e:
                    # logger.warning(
                    #     f"[Frame Missing] Vehicle {vehicle.vehicle_id} missing frame {frame_num}. "
                    #     f"Initial frame: {vehicle.initial_frame}, Final frame: {vehicle.final_frame}. "
                    #     f"Error: {e}"
                    # )
                    continue
                if state is not None:
                    svs_state.append(state)
        return svs_state


class Vehicle:
    def __init__(self, track):
        self.track = track
        self.initial_frame = int(track[FRAME].min())
        self.final_frame = int(track[FRAME].max())
        self.vehicle_id = track[TRACK_ID][0]
