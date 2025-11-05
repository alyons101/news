import { useEffect, useState } from 'react';

const STORAGE_KEY = 'aurora-recent-searches';

export function useRecentSearches() {
  const [recent, setRecent] = useState<string[]>([]);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        setRecent(JSON.parse(stored));
      } catch (error) {
        console.warn('Failed to parse recent searches', error);
      }
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(recent));
  }, [recent]);

  const addRecent = (symbol: string) => {
    setRecent((prev) => {
      const filtered = prev.filter((item) => item !== symbol);
      return [symbol, ...filtered].slice(0, 10);
    });
  };

  return { recent, addRecent };
}
