import { fetchData } from 'apis/common.api';

class WarehouseService {
  fetchWarehouses = async () => {
    return fetchData('/warehouses/');
  };

  getWarehouse = async (id: any) => {
    const data = await fetchData(`/warehouses/${id}/`);
    return data;
  };
}

const warehouseService = new WarehouseService();

export default warehouseService;
