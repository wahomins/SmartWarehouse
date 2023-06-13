import { fetchData } from 'apis/common.api';

class CommonService {
  callGet = async (route: string) => {
    return fetchData(route);
  };
}

const commonService = new CommonService();

export default commonService;
