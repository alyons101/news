const BASE_URL = '/api';

type Method = 'GET' | 'POST';

const request = async (path: string, method: Method = 'GET', body?: any) => {
  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json'
    },
    body: body ? JSON.stringify(body) : undefined
  });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
};

export const fetchSearch = async (query: string) => {
  if (!query) return [];
  return request(`/search?query=${encodeURIComponent(query)}`);
};

export const fetchCompany = async (symbol: string) => {
  return request(`/companies/${symbol}`);
};

export const fetchComparison = async (symbols: string[]) => {
  return request('/compare', 'POST', { symbols });
};
