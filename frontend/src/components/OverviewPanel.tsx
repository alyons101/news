import { ExternalLink, Globe2, MapPin } from 'lucide-react';

import { FinancialsResponse, MetricCard } from '../types';
import { Card, CardContent, CardTitle } from './ui/card';
import { Skeleton } from './ui/skeleton';

interface OverviewPanelProps {
  data?: FinancialsResponse;
  loading: boolean;
}

export function OverviewPanel({ data, loading }: OverviewPanelProps) {
  const metrics = data?.metrics ?? [];
  const profile = data?.profile;

  return (
    <Card className="col-span-12 lg:col-span-4">
      <CardTitle>Company Overview</CardTitle>
      <CardContent>
        {loading && (
          <div className="space-y-3">
            <Skeleton className="h-6 w-1/2" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
          </div>
        )}
        {!loading && profile && (
          <div className="space-y-4">
            <div>
              <h2 className="text-2xl font-semibold text-slate-100">{profile.name}</h2>
              <p className="text-sm text-slate-400">
                {profile.symbol} • {profile.exchange} • {profile.sector}
              </p>
            </div>
            <p className="text-sm leading-relaxed text-slate-300 line-clamp-4">{profile.description}</p>
            <div className="grid grid-cols-2 gap-3">
              {metrics.map((metric: MetricCard) => (
                <div key={metric.label} className="rounded-lg border border-slate-800/70 bg-black/20 p-3">
                  <p className="text-xs uppercase tracking-wide text-slate-500">{metric.label}</p>
                  <p className="mt-1 text-lg font-semibold text-slate-100">{metric.value}</p>
                  {metric.hint && <p className="text-xs text-slate-500">{metric.hint}</p>}
                </div>
              ))}
            </div>
            <div className="flex flex-wrap items-center gap-3 text-sm text-slate-400">
              {profile.country && (
                <span className="flex items-center gap-1"><MapPin className="h-4 w-4" /> {profile.country}</span>
              )}
              {profile.website && (
                <a href={profile.website} target="_blank" rel="noreferrer" className="flex items-center gap-1 text-accent">
                  <Globe2 className="h-4 w-4" /> Website
                </a>
              )}
              <a
                href={`https://finance.yahoo.com/quote/${profile.symbol}`}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 rounded-lg border border-slate-700 px-3 py-1 text-xs text-slate-300 transition hover:border-accent hover:text-accent"
              >
                <ExternalLink className="h-3 w-3" /> Open in Yahoo Finance
              </a>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
