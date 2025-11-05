export interface MetricCard {
  label: string;
  value: string;
  delta?: number;
  hint?: string;
}

export interface CompanyProfile {
  symbol: string;
  name: string;
  currency?: string;
  exchange?: string;
  sector?: string;
  industry?: string;
  marketCap?: number;
  website?: string;
  country?: string;
  description?: string;
}

export interface FinancialStatement {
  period: string;
  data: Record<string, number>;
}

export interface FinancialsResponse {
  symbol: string;
  profile: CompanyProfile;
  metrics: MetricCard[];
  statements: {
    income: FinancialStatement[];
    balance: FinancialStatement[];
    cashflow: FinancialStatement[];
  };
  filings: Array<{
    accessionNumber: string;
    formType: string;
    filedAt: string;
    reportUrl?: string;
  }>;
}

export interface PricePoint {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface ChartResponse {
  symbol: string;
  range: string;
  interval: string;
  prices: PricePoint[];
  indicators: Record<string, { name: string; data: Array<Record<string, number | string>> }>;
}

export interface NewsItem {
  title: string;
  url: string;
  source?: string;
  summary?: string;
  publishedAt: string;
  thumbnail?: string;
  videoUrl?: string;
}

export interface NewsResponse {
  symbol: string;
  items: NewsItem[];
}

export interface VideoItem {
  id: string;
  title: string;
  url: string;
  videoUrl: string;
  channel?: string;
  description?: string;
  publishedAt: string;
  thumbnail?: string;
}

export interface VideosResponse {
  query: string;
  items: VideoItem[];
}

export interface InsightsResponse {
  symbol: string;
  highlights: string[];
  metrics: MetricCard[];
  narrative: string;
  relatedNews: NewsItem[];
  technicalView: Record<string, any>;
}

export interface ComparisonResponse {
  entries: Array<{
    symbol: string;
    profile: CompanyProfile;
    metrics: MetricCard[];
  }>;
  correlations: Record<string, number>;
}

export interface AnalyzeResponse {
  summary: string;
  source: string;
}
