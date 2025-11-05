import { useEffect, useState } from 'react';
import { Search } from 'lucide-react';

import { useRecentSearches } from '../hooks/useRecentSearches';
import { api } from '../services/api';
import { Input } from './ui/input';
import { cn } from '../lib/utils';
import { Button } from './ui/button';

interface SearchBarProps {
  value: string;
  onSelect: (symbol: string) => void;
  onPin: (symbol: string) => void;
}

export function SearchBar({ value, onSelect, onPin }: SearchBarProps) {
  const [query, setQuery] = useState(value);
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const { recent, addRecent } = useRecentSearches();

  useEffect(() => {
    setQuery(value);
  }, [value]);

  useEffect(() => {
    if (!query || query.length < 1) {
      setResults([]);
      return;
    }
    const timeout = setTimeout(async () => {
      setLoading(true);
      try {
        const response = await api.searchSymbols(query);
        setResults(response || []);
      } catch (error) {
        console.warn('Search failed', error);
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, 250);
    return () => clearTimeout(timeout);
  }, [query]);

  const selectSymbol = (symbol: string) => {
    onSelect(symbol);
    addRecent(symbol);
    setQuery(symbol);
    setResults([]);
  };

  return (
    <div className="relative w-full">
      <div className="relative flex items-center">
        <Search className="absolute left-4 h-4 w-4 text-slate-500" />
        <Input
          value={query}
          onChange={(event) => setQuery(event.target.value.toUpperCase())}
          onFocus={() => query && setResults(results)}
          placeholder="Search tickers, companies, or assets"
          className="pl-10"
        />
        <Button variant="ghost" className="ml-3" onClick={() => query && onPin(query.toUpperCase())}>
          + Watch
        </Button>
      </div>
      {(results.length > 0 || recent.length > 0) && (
        <div className="absolute z-20 mt-2 w-full rounded-xl border border-slate-800 bg-panel/95 p-3 shadow-glow">
          <div className="space-y-1">
            {results.length > 0 && (
              <p className="text-xs uppercase tracking-wide text-slate-500">Matches</p>
            )}
            {results.map((item) => (
              <button
                key={item.symbol}
                onClick={() => selectSymbol(item.symbol)}
                className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-left transition hover:bg-white/10"
              >
                <span className="font-medium">{item.symbol}</span>
                <span className="text-xs text-slate-400">{item.name}</span>
              </button>
            ))}
            {loading && <p className="text-xs text-slate-500">Searching…</p>}
            {recent.length > 0 && (
              <div className={cn('pt-2', results.length > 0 && 'border-t border-slate-800')}>
                <p className="text-xs uppercase tracking-wide text-slate-500">Recent</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {recent.map((symbol) => (
                    <button
                      key={symbol}
                      onClick={() => selectSymbol(symbol)}
                      className="rounded-full border border-slate-700 px-3 py-1 text-xs text-slate-300 transition hover:border-accent hover:text-accent"
                    >
                      {symbol}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
