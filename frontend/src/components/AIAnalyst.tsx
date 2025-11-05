import { useMutation } from '@tanstack/react-query';
import { Bot, Loader2 } from 'lucide-react';
import { useState } from 'react';

import { InsightsResponse } from '../types';
import { api } from '../services/api';
import { Card, CardContent, CardTitle } from './ui/card';
import { Button } from './ui/button';

interface AIAnalystProps {
  symbol: string;
  insights?: InsightsResponse;
}

export function AIAnalyst({ symbol, insights }: AIAnalystProps) {
  const [question, setQuestion] = useState('Explain today’s price action and key drivers.');
  const mutation = useMutation({
    mutationFn: (prompt: string) =>
      api.analyzeSymbol({
        symbol,
        question: prompt,
        context: {
          highlights: insights?.highlights,
          technical: insights?.technicalView,
          headline: insights?.relatedNews?.[0]?.title,
        },
      }),
  });

  return (
    <Card className="col-span-12 xl:col-span-4">
      <CardTitle className="flex items-center gap-2">
        <Bot className="h-4 w-4 text-accent" /> AI Market Analyst
      </CardTitle>
      <CardContent className="mt-4 space-y-4">
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          className="w-full rounded-lg border border-slate-800 bg-black/30 p-3 text-sm text-slate-200 focus:border-accent focus:outline-none"
          rows={3}
        />
        <Button
          onClick={() => mutation.mutate(question)}
          disabled={mutation.isPending}
          className="w-full"
        >
          {mutation.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Run Analysis'}
        </Button>
        {mutation.data && (
          <div className="rounded-lg border border-slate-800/70 bg-black/20 p-4 text-sm text-slate-200">
            {mutation.data.summary}
            <p className="mt-2 text-xs text-slate-500">Source: {mutation.data.source}</p>
          </div>
        )}
        {mutation.error && (
          <p className="text-sm text-rose-400">
            {(mutation.error as Error).message || 'Analysis failed'}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
