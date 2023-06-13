import httpRequest from 'services/httpRequest';

export const fetchTodo = async (url: string) => {
  return httpRequest.get(url, {
    showSpinner: true,
  });
};

export const fetchMultiRequest = async (url: string) => {
  return httpRequest.get(url);
};

export const fetchData = async (url: string) => {
  const resp = await httpRequest.get(url, {
    showSpinner: true,
  });
  return resp.data;
};
