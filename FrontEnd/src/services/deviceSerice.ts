import { fetchData } from 'apis/common.api';

class DeviceService {
  fetchDevices = async () => {
    return fetchData('/devices/');
  };

  fetchDeviceLogs = async () => {
    const data = await fetchData('/devices/logs/activity/');

    return data;
  };
}

const deviceService = new DeviceService();

export default deviceService;
