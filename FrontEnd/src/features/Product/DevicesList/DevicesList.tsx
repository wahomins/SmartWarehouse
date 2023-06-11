import React from 'react';
import SimpleGrid from 'components/SimpleGrid';
import { PATH_NAME } from 'configs';

export default function ProductList() {
  const header = 'Product';
  const pathName = PATH_NAME.PRODUCT_ADD;
  const actions = [{ resource: 'product', action: 'create' }];
  const pagination = {
    pageNumber: 1,
    itemsPerPage: 10,
  };
  const table = {
    rows: [
      { name: 'Frozen yoghurt', calories: 159, fat: 6.0, carbs: 24, protein: 4.0 },
      { name: 'Ice cream sandwich', calories: 237, fat: 9.0, carbs: 37, protein: 4.3 },
      { name: 'Eclair', calories: 262, fat: 16.0, carbs: 24, protein: 6.0 },
      { name: 'Cupcake', calories: 305, fat: 3.7, carbs: 67, protein: 4.3 },
      { name: 'Gingerbread', calories: 356, fat: 16.0, carbs: 49, protein: 3.9 },
    ],
    headers: [
      { columnName: 'Dessert (100g serving)', key: 'name' },
      { columnName: 'Calories', key: 'calories' },
      { columnName: 'Fat (g)', key: 'fat' },
      { columnName: 'Carbs (g)', key: 'carbs' },
      { columnName: 'Protein (g)', key: 'protein' },
    ],
  };

  return <SimpleGrid header={header} addPathName={pathName} actions={actions} pagination={pagination} table={table} />;
}
