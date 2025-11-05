const BASE_URL = '/api';

type Method = 'GET' | 'POST';

async function request<T>(path: string, method: Method = 'GET', body?: unknown): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json'
    },
    body: body ? JSON.stringify(body) : undefined
  });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }
  return response.json();
}

export const api = {
  searchSymbols: (query: string) => request(`/search?query=${encodeURIComponent(query)}`),
  getFinancials: (symbol: string) => request(`/financials/${symbol}`),
  getChart: (symbol: string, params: { range?: string; interval?: string } = {}) => {
    const searchParams = new URLSearchParams();
    if (params.range) searchParams.set('range', params.range);
    if (params.interval) searchParams.set('interval', params.interval);
    const query = searchParams.toString();
    return request(`/chart/${symbol}${query ? `?${query}` : ''}`);
  },
  getNews: (symbol: string) => request(`/news/${symbol}`),
  getInsights: (symbol: string) => request(`/insights/${symbol}`),
  compareSymbols: (symbols: string[]) => request('/compare', 'POST', { symbols }),
  analyzeSymbol: (payload: { symbol: string; question?: string; context?: any }) =>
    request('/analyze', 'POST', payload)
};
