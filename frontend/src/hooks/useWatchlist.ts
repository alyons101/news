import { useEffect, useState } from 'react';

const STORAGE_KEY = 'aurora-watchlist';

export function useWatchlist() {
  const [symbols, setSymbols] = useState<string[]>([]);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        setSymbols(JSON.parse(stored));
      } catch (error) {
        console.warn('Failed to parse watchlist', error);
      }
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(symbols));
  }, [symbols]);

  const addSymbol = (symbol: string) => {
    setSymbols((prev) => {
      if (prev.includes(symbol)) return prev;
      return [...prev, symbol].slice(-20);
    });
  };

  const removeSymbol = (symbol: string) => {
    setSymbols((prev) => prev.filter((item) => item !== symbol));
  };

  return { symbols, addSymbol, removeSymbol };
}
