import { FormEvent, useState } from 'react';

import { ComparisonResponse } from '../types';
import { Card, CardContent, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Skeleton } from './ui/skeleton';

interface ComparisonPanelProps {
  data?: ComparisonResponse;
  loading: boolean;
  onAddSymbol: (symbol: string) => void;
}

export function ComparisonPanel({ data, loading, onAddSymbol }: ComparisonPanelProps) {
  const [value, setValue] = useState('');

  const submit = (event: FormEvent) => {
    event.preventDefault();
    if (!value) return;
    onAddSymbol(value.toUpperCase());
    setValue('');
  };

  return (
    <Card className="col-span-12 xl:col-span-4">
      <div className="flex items-center justify-between">
        <CardTitle>Peer Comparison</CardTitle>
        <form onSubmit={submit} className="flex items-center gap-2">
          <Input
            value={value}
            onChange={(event) => setValue(event.target.value)}
            placeholder="Add symbol"
            className="h-9 w-24 text-xs"
          />
          <Button size="sm" type="submit">
            Add
          </Button>
        </form>
      </div>
      <CardContent className="mt-4 space-y-4">
        {loading && <Skeleton className="h-48 w-full" />}
        {!loading && data && (
          <div className="space-y-4">
            <div className="grid gap-3">
              {data.entries.map((entry) => (
                <div key={entry.symbol} className="rounded-lg border border-slate-800/70 bg-black/20 p-4">
                  <div className="flex items-center justify-between text-sm">
                    <div>
                      <p className="font-semibold text-slate-100">{entry.profile.name}</p>
                      <p className="text-xs text-slate-500">{entry.symbol} • {entry.profile.sector}</p>
                    </div>
                    <div className="text-xs text-slate-400">{entry.profile.exchange}</div>
                  </div>
                  <div className="mt-3 grid grid-cols-2 gap-3 text-sm">
                    {entry.metrics.map((metric) => (
                      <div key={metric.label} className="rounded-md border border-slate-800/60 bg-black/10 p-2">
                        <p className="text-xs uppercase tracking-wide text-slate-500">{metric.label}</p>
                        <p className="font-semibold text-slate-100">{metric.value}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
            <div className="rounded-lg border border-slate-800/70 bg-black/10 p-4 text-sm text-slate-300">
              <p className="text-xs uppercase tracking-wide text-slate-500">Correlations</p>
              <div className="mt-2 space-y-1">
                {Object.entries(data.correlations).map(([pair, value]) => (
                  <div key={pair} className="flex justify-between">
                    <span>{pair}</span>
                    <span>{value.toFixed(2)}</span>
                  </div>
                ))}
                {Object.keys(data.correlations).length === 0 && <p className="text-xs text-slate-500">Not enough price history.</p>}
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
