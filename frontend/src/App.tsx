import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Activity } from 'lucide-react';
import { motion } from 'framer-motion';

import { SearchBar } from './components/SearchBar';
import { Sidebar } from './components/Sidebar';
import { OverviewPanel } from './components/OverviewPanel';
import { ChartPanel } from './components/ChartPanel';
import { FinancialPanel } from './components/FinancialPanel';
import { InsightsPanel } from './components/InsightsPanel';
import { NewsPanel } from './components/NewsPanel';
import { ComparisonPanel } from './components/ComparisonPanel';
import { AIAnalyst } from './components/AIAnalyst';
import { useWatchlist } from './hooks/useWatchlist';
import { api } from './services/api';
import { InsightsResponse } from './types';

function App() {
  const [symbol, setSymbol] = useState('AAPL');
  const [chartRange, setChartRange] = useState('1y');
  const [peerSymbols, setPeerSymbols] = useState<string[]>(['MSFT']);
  const { symbols: watchlist, addSymbol, removeSymbol } = useWatchlist();

  const financialsQuery = useQuery({
    queryKey: ['financials', symbol],
    queryFn: () => api.getFinancials(symbol),
  });

  const chartQuery = useQuery({
    queryKey: ['chart', symbol, chartRange],
    queryFn: () => api.getChart(symbol, { range: chartRange }),
  });

  const newsQuery = useQuery({
    queryKey: ['news', symbol],
    queryFn: () => api.getNews(symbol),
  });

  const insightsQuery = useQuery<InsightsResponse>({
    queryKey: ['insights', symbol],
    queryFn: () => api.getInsights(symbol),
  });

  const comparisonSymbols = useMemo(() => {
    const base = [symbol, ...peerSymbols];
    return Array.from(new Set(base.map((item) => item.toUpperCase())));
  }, [symbol, peerSymbols]);

  const comparisonQuery = useQuery({
    queryKey: ['compare', comparisonSymbols],
    queryFn: () => api.compareSymbols(comparisonSymbols),
    enabled: comparisonSymbols.length > 0,
  });

  const handleSelectSymbol = (next: string) => {
    setSymbol(next.toUpperCase());
  };

  const handleAddPeer = (candidate: string) => {
    if (!candidate || candidate.toUpperCase() === symbol) return;
    setPeerSymbols((prev) => Array.from(new Set([...prev, candidate.toUpperCase()])));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-100">
      <div className="mx-auto flex max-w-[1400px] flex-col gap-8 px-6 py-8 lg:flex-row">
        <Sidebar watchlist={watchlist} onSelect={handleSelectSymbol} onRemove={removeSymbol} />
        <main className="flex-1 space-y-6">
          <header className="space-y-4">
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <SearchBar value={symbol} onSelect={handleSelectSymbol} onPin={(ticker) => addSymbol(ticker.toUpperCase())} />
              <div className="flex items-center gap-2 rounded-xl border border-slate-800/80 bg-black/20 px-4 py-2 text-xs uppercase tracking-wide text-slate-400">
                <Activity className="h-4 w-4 text-accent" />
                Real-time market intelligence for {symbol.toUpperCase()}
              </div>
            </div>
          </header>
          <motion.section
            className="grid grid-cols-12 gap-6"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, ease: 'easeOut' }}
          >
            <OverviewPanel data={financialsQuery.data} loading={financialsQuery.isLoading} />
            <ChartPanel
              data={chartQuery.data}
              loading={chartQuery.isLoading}
              selectedRange={chartRange}
              onChangeRange={(value) => setChartRange(value)}
            />
            <FinancialPanel data={financialsQuery.data} loading={financialsQuery.isLoading} />
            <InsightsPanel data={insightsQuery.data} loading={insightsQuery.isLoading} />
            <NewsPanel data={newsQuery.data} loading={newsQuery.isLoading} />
            <ComparisonPanel
              data={comparisonQuery.data}
              loading={comparisonQuery.isLoading}
              onAddSymbol={handleAddPeer}
            />
            <AIAnalyst symbol={symbol} insights={insightsQuery.data} />
          </motion.section>
        </main>
      </div>
    </div>
  );
}

export default App;
