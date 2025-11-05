import { useMemo, useState } from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid, BarChart, Bar } from 'recharts';

import { ChartResponse } from '../types';
import { Card, CardContent, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Skeleton } from './ui/skeleton';

interface ChartPanelProps {
  data?: ChartResponse;
  loading: boolean;
  selectedRange: string;
  onChangeRange: (value: string) => void;
}

const ranges = [
  { label: '1M', value: '1mo' },
  { label: '3M', value: '3mo' },
  { label: '1Y', value: '1y' },
  { label: '5Y', value: '5y' }
];

export function ChartPanel({ data, loading, selectedRange, onChangeRange }: ChartPanelProps) {
  const [selectedIndicator, setSelectedIndicator] = useState<'macd' | 'rsi' | 'bollinger'>('macd');

  const priceSeries = useMemo(() => {
    if (!data) return [];
    return data.prices.map((point) => ({
      ...point,
      timestamp: new Date(point.timestamp).toLocaleDateString(),
    }));
  }, [data]);

  const indicatorSeries = data?.indicators[selectedIndicator]?.data ?? [];

  return (
    <Card className="col-span-12 lg:col-span-8 xl:col-span-8">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <CardTitle>Market Performance</CardTitle>
        <div className="flex flex-wrap gap-2">
          {ranges.map((range) => (
            <Button
              key={range.value}
              size="sm"
              variant={selectedRange === range.value ? 'default' : 'ghost'}
              onClick={() => onChangeRange(range.value)}
            >
              {range.label}
            </Button>
          ))}
        </div>
      </div>
      <CardContent className="mt-6 space-y-6">
        {loading && <Skeleton className="h-64 w-full" />}
        {!loading && priceSeries.length > 0 && (
          <div className="grid gap-6 xl:grid-cols-5">
            <div className="xl:col-span-3">
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={priceSeries}>
                  <defs>
                    <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#38bdf8" stopOpacity={0.3} />
                      <stop offset="100%" stopColor="#38bdf8" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="rgba(148,163,184,0.1)" strokeDasharray="3 3" />
                  <XAxis dataKey="timestamp" stroke="#64748b" hide />
                  <YAxis stroke="#64748b" domain={['auto', 'auto']} />
                  <Tooltip
                    contentStyle={{
                      background: '#0f172a',
                      border: '1px solid #1e293b',
                      borderRadius: '0.75rem',
                      color: '#e2e8f0'
                    }}
                  />
                  <Area type="monotone" dataKey="close" stroke="#38bdf8" strokeWidth={2} fill="url(#priceGradient)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <div className="space-y-3 xl:col-span-2">
              <div className="flex gap-2">
                {(['macd', 'rsi', 'bollinger'] as const).map((indicator) => (
                  <Button
                    key={indicator}
                    size="sm"
                    variant={selectedIndicator === indicator ? 'default' : 'ghost'}
                    onClick={() => setSelectedIndicator(indicator)}
                  >
                    {indicator.toUpperCase()}
                  </Button>
                ))}
              </div>
              <div className="rounded-xl border border-slate-800/80 bg-black/20 p-4">
                <h4 className="text-sm font-semibold uppercase tracking-wide text-slate-400">{selectedIndicator.toUpperCase()}</h4>
                {indicatorSeries.length === 0 && <p className="mt-3 text-sm text-slate-500">Indicator data not available.</p>}
                {indicatorSeries.length > 0 && (
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={indicatorSeries.slice().reverse()}>
                      <XAxis dataKey="timestamp" hide />
                      <YAxis stroke="#64748b" domain={['auto', 'auto']} />
                      <Tooltip
                        contentStyle={{
                          background: '#0f172a',
                          border: '1px solid #1e293b',
                          borderRadius: '0.75rem',
                          color: '#e2e8f0'
                        }}
                      />
                      <Bar dataKey={selectedIndicator === 'rsi' ? 'value' : selectedIndicator === 'macd' ? 'hist' : 'middle'} fill="#38bdf8" />
                    </BarChart>
                  </ResponsiveContainer>
                )}
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
