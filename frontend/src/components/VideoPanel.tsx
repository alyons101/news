import ReactPlayer from 'react-player/lazy';
import { CalendarClock, ExternalLink } from 'lucide-react';

import { VideosResponse } from '../types';
import { Card, CardContent, CardTitle } from './ui/card';
import { Skeleton } from './ui/skeleton';

interface VideoPanelProps {
  data?: VideosResponse;
  loading: boolean;
}

export function VideoPanel({ data, loading }: VideoPanelProps) {
  const items = data?.items ?? [];
  const featured = items[0];
  const secondary = items.slice(1, 5);

  return (
    <Card className="col-span-12 xl:col-span-4">
      <CardTitle>Market Video Briefings</CardTitle>
      <CardContent className="mt-4 space-y-4">
        {loading && (
          <div className="space-y-3">
            <Skeleton className="h-40 w-full" />
            <Skeleton className="h-4 w-2/3" />
            <Skeleton className="h-4 w-1/2" />
          </div>
        )}
        {!loading && featured && (
          <div className="space-y-3">
            <div className="overflow-hidden rounded-xl border border-slate-800/70">
              <ReactPlayer
                url={featured.videoUrl}
                width="100%"
                height="220px"
                controls
                light={featured.thumbnail ?? true}
              />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-slate-100">{featured.title}</h3>
              <p className="mt-2 text-sm text-slate-400">{featured.description}</p>
              <div className="mt-2 flex items-center gap-2 text-xs uppercase tracking-wide text-slate-500">
                {featured.channel} • {new Date(featured.publishedAt).toLocaleString()}
              </div>
            </div>
          </div>
        )}
        <div className="space-y-3">
          {secondary.map((item) => (
            <a
              key={item.id}
              href={item.url}
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-3 rounded-lg border border-slate-800/60 bg-black/20 p-3 transition hover:border-accent"
            >
              {item.thumbnail ? (
                <img src={item.thumbnail} alt="Video thumbnail" className="h-14 w-24 rounded-md object-cover" />
              ) : (
                <div className="flex h-14 w-24 items-center justify-center rounded-md bg-slate-900 text-slate-500">
                  <ExternalLink className="h-5 w-5" />
                </div>
              )}
              <div className="flex-1">
                <p className="text-sm font-semibold text-slate-100 line-clamp-2">{item.title}</p>
                <div className="mt-2 flex items-center gap-2 text-xs text-slate-500">
                  <CalendarClock className="h-3.5 w-3.5" />
                  {new Date(item.publishedAt).toLocaleString()}
                </div>
              </div>
            </a>
          ))}
          {!loading && items.length === 0 && (
            <p className="text-sm text-slate-500">No recent videos available for this query.</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
