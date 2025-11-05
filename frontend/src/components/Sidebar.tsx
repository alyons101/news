import { Bookmark, Trash2 } from 'lucide-react';

import { Button } from './ui/button';
import { Card, CardContent, CardTitle } from './ui/card';

interface SidebarProps {
  watchlist: string[];
  onSelect: (symbol: string) => void;
  onRemove: (symbol: string) => void;
}

export function Sidebar({ watchlist, onSelect, onRemove }: SidebarProps) {
  return (
    <aside className="hidden w-64 flex-col gap-4 lg:flex">
      <Card className="flex-1">
        <CardTitle className="flex items-center gap-2">
          <Bookmark className="h-4 w-4" /> Watchlist
        </CardTitle>
        <CardContent className="mt-4 space-y-2">
          {watchlist.length === 0 && <p className="text-sm text-slate-500">Pin tickers to curate your private list.</p>}
          {watchlist.map((symbol) => (
            <div key={symbol} className="flex items-center justify-between rounded-lg border border-slate-800/80 bg-black/20 px-3 py-2">
              <button onClick={() => onSelect(symbol)} className="text-sm font-semibold tracking-wide text-slate-100">
                {symbol}
              </button>
              <Button size="sm" variant="ghost" className="h-8 px-2 text-slate-500" onClick={() => onRemove(symbol)}>
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </CardContent>
      </Card>
    </aside>
  );
}
