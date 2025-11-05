import { Sparkles } from 'lucide-react';

import { InsightsResponse } from '../types';
import { Card, CardContent, CardTitle } from './ui/card';
import { Skeleton } from './ui/skeleton';

interface InsightsPanelProps {
  data?: InsightsResponse;
  loading: boolean;
}

export function InsightsPanel({ data, loading }: InsightsPanelProps) {
  const highlights = data?.highlights ?? [];
  const technical = data?.technicalView ?? {};

  return (
    <Card className="col-span-12 xl:col-span-4">
      <CardTitle className="flex items-center gap-2">
        <Sparkles className="h-4 w-4 text-accent" /> Aurora Insights
      </CardTitle>
      <CardContent className="mt-4 space-y-4">
        {loading && <Skeleton className="h-32 w-full" />}
        {!loading && (
          <>
            <div>
              <h4 className="text-xs uppercase tracking-wide text-slate-500">Highlights</h4>
              <ul className="mt-2 space-y-2 text-sm text-slate-300">
                {highlights.map((highlight) => (
                  <li key={highlight} className="flex gap-2">
                    <span className="mt-1 h-1.5 w-1.5 rounded-full bg-accent" />
                    <span>{highlight}</span>
                  </li>
                ))}
              </ul>
            </div>
            {data?.narrative && (
              <div className="rounded-lg border border-slate-800/70 bg-black/20 p-4 text-sm text-slate-300">
                {data.narrative}
              </div>
            )}
            {technical && Object.keys(technical).length > 0 && (
              <div className="grid gap-3 text-sm">
                {Object.entries(technical).map(([key, payload]) => (
                  <div key={key} className="rounded-lg border border-slate-800/60 bg-black/10 p-3">
                    <p className="text-xs uppercase tracking-wide text-slate-500">{key.toUpperCase()}</p>
                    <p className="mt-1 text-slate-200">{(payload as any).narrative}</p>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}
