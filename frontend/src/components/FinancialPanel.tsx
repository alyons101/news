import { useMemo, useState } from 'react';

import { FinancialsResponse } from '../types';
import { Card, CardContent, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Skeleton } from './ui/skeleton';
import { ScrollArea } from './ui/scroll-area';

interface FinancialPanelProps {
  data?: FinancialsResponse;
  loading: boolean;
}

const tabs = [
  { label: 'Income Statement', key: 'income' },
  { label: 'Balance Sheet', key: 'balance' },
  { label: 'Cash Flow', key: 'cashflow' }
];

export function FinancialPanel({ data, loading }: FinancialPanelProps) {
  const [activeTab, setActiveTab] = useState<(typeof tabs)[number]['key']>('income');

  const statement = useMemo(() => {
    if (!data) return [];
    return data.statements[activeTab] ?? [];
  }, [data, activeTab]);

  const headers = statement.length > 0 ? Object.keys(statement[0].data) : [];

  return (
    <Card className="col-span-12 xl:col-span-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <CardTitle>Financial Statements</CardTitle>
        <div className="flex gap-2">
          {tabs.map((tab) => (
            <Button
              key={tab.key}
              size="sm"
              variant={activeTab === tab.key ? 'default' : 'ghost'}
              onClick={() => setActiveTab(tab.key)}
            >
              {tab.label}
            </Button>
          ))}
        </div>
      </div>
      <CardContent className="mt-4">
        {loading && <Skeleton className="h-48 w-full" />}
        {!loading && statement.length === 0 && <p className="text-sm text-slate-500">No data available.</p>}
        {!loading && statement.length > 0 && (
          <ScrollArea className="max-h-80">
            <table className="w-full min-w-[500px] text-sm">
              <thead className="sticky top-0 bg-panel">
                <tr className="text-left text-xs uppercase tracking-wide text-slate-400">
                  <th className="px-3 py-2">Period</th>
                  {headers.map((header) => (
                    <th key={header} className="px-3 py-2">
                      {header.replace(/([A-Z])/g, ' $1').trim()}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {statement.map((row) => (
                  <tr key={row.period} className="border-t border-slate-800/50">
                    <td className="px-3 py-2 text-slate-400">{row.period}</td>
                    {headers.map((header) => (
                      <td key={header} className="px-3 py-2">
                        {Intl.NumberFormat('en-US', { notation: 'compact', maximumFractionDigits: 2 }).format(
                          row.data[header] ?? 0
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </ScrollArea>
        )}
      </CardContent>
    </Card>
  );
}
