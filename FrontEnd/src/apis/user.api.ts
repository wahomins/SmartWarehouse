import httpRequest from 'services/httpRequest';

export const login = async (url: string, data: any) => {
  const resp = await httpRequest.post(url, data, {
    showSpinner: true,
  });
  return resp.data;
};
