import { fetchData } from 'apis/common.api';

class DeviceService {
  fetchDevices = async () => {
    return fetchData('/devices/');
  };
}

const deviceService = new DeviceService();

export default deviceService;
