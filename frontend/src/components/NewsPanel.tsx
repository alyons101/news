import ReactPlayer from 'react-player/lazy';
import { CalendarDays, Play } from 'lucide-react';

import { NewsResponse } from '../types';
import { Card, CardContent, CardTitle } from './ui/card';
import { Skeleton } from './ui/skeleton';

interface NewsPanelProps {
  data?: NewsResponse;
  loading: boolean;
}

export function NewsPanel({ data, loading }: NewsPanelProps) {
  const items = data?.items ?? [];
  const featured = items.find((item) => item.videoUrl) ?? items[0];
  const secondary = items.filter((item) => item !== featured).slice(0, 6);

  return (
    <Card className="col-span-12 xl:col-span-4">
      <CardTitle>Market Coverage</CardTitle>
      <CardContent className="mt-4 space-y-4">
        {loading && (
          <div className="space-y-3">
            <Skeleton className="h-40 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-1/2" />
          </div>
        )}
        {!loading && featured && (
          <div className="space-y-3">
            {featured.videoUrl ? (
              <div className="relative overflow-hidden rounded-xl border border-slate-800/70">
                <ReactPlayer url={featured.videoUrl} width="100%" height="220px" controls light={featured.thumbnail ?? true} />
              </div>
            ) : (
              <div className="relative overflow-hidden rounded-xl border border-slate-800/70 bg-black/40 p-6">
                <Play className="mb-3 h-6 w-6 text-accent" />
                <h3 className="text-lg font-semibold text-slate-100">{featured.title}</h3>
                <p className="mt-2 text-sm text-slate-400">{featured.summary}</p>
              </div>
            )}
            <div className="text-xs uppercase tracking-wide text-slate-500">
              {featured.source} • {new Date(featured.publishedAt).toLocaleString()}
            </div>
          </div>
        )}
        <div className="space-y-3">
          {secondary.map((item) => (
            <a
              key={item.title}
              href={item.url}
              target="_blank"
              rel="noreferrer"
              className="block rounded-lg border border-slate-800/60 bg-black/20 p-3 transition hover:border-accent"
            >
              <p className="text-sm font-semibold text-slate-100">{item.title}</p>
              <p className="mt-1 text-xs text-slate-500">{item.source}</p>
              <div className="mt-2 flex items-center gap-1 text-xs text-slate-500">
                <CalendarDays className="h-3 w-3" /> {new Date(item.publishedAt).toLocaleString()}
              </div>
            </a>
          ))}
          {!loading && items.length === 0 && <p className="text-sm text-slate-500">No news available for this symbol.</p>}
        </div>
      </CardContent>
    </Card>
  );
}
