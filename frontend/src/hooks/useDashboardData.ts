import { useEffect, useState } from 'react';
import { fetchCompany } from '../services/api';

export const useDashboardData = (symbol: string) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const response = await fetchCompany(symbol);
      setData(response);
      setLoading(false);
    };
    load();
  }, [symbol]);

  return { data, loading };
};
