import { Card, CardContent, CircularProgress, Stack, ToggleButton, ToggleButtonGroup, Typography } from '@mui/material';
import { useMemo, useState } from 'react';
import {
  Area,
  AreaChart,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Bar
} from 'recharts';

interface Props {
  data: any;
  loading: boolean;
}

const ChartPanel = ({ data, loading }: Props) => {
  const [mode, setMode] = useState<'price' | 'technicals'>('price');

  const priceSeries = useMemo(() => {
    if (!data) return [];
    return data.incomeStatement.map((row: any) => ({
      name: row.year,
      revenue: row.revenue,
      netIncome: row.netIncome,
      eps: row.eps
    }));
  }, [data]);

  const macdSeries = useMemo(() => {
    if (!data) return [];
    return data.technicals.macd.map((entry: any, index: number) => ({
      index,
      macd: entry.macd,
      signal: entry.signal,
      histogram: entry.histogram
    }));
  }, [data]);

  if (loading || !data) {
    return (
      <Card sx={{ backgroundColor: 'rgba(20,24,38,0.85)', height: 340 }}>
        <CardContent sx={{ display: 'flex', justifyContent: 'center' }}>
          <CircularProgress size={28} />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ backgroundColor: 'rgba(20,24,38,0.85)', height: 340 }}>
      <CardContent sx={{ height: '100%' }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">Visualization</Typography>
          <ToggleButtonGroup exclusive value={mode} onChange={(_, value) => value && setMode(value)}>
            <ToggleButton value="price">Fundamentals</ToggleButton>
            <ToggleButton value="technicals">Technicals</ToggleButton>
          </ToggleButtonGroup>
        </Stack>
        <ResponsiveContainer width="100%" height="90%">
          {mode === 'price' ? (
            <ComposedChart data={priceSeries}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
              <XAxis dataKey="name" stroke="#9aa4bf" />
              <YAxis yAxisId="left" stroke="#9aa4bf" />
              <YAxis yAxisId="right" orientation="right" stroke="#9aa4bf" />
              <Tooltip contentStyle={{ backgroundColor: '#1b2333', border: 'none' }} />
              <Legend />
              <Bar dataKey="revenue" barSize={18} fill="#00bcd4" yAxisId="left" name="Revenue" />
              <Bar dataKey="netIncome" barSize={18} fill="#4caf50" yAxisId="left" name="Net Income" />
              <Line type="monotone" dataKey="eps" stroke="#ff9800" yAxisId="right" name="EPS" />
            </ComposedChart>
          ) : (
            <AreaChart data={macdSeries}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
              <XAxis dataKey="index" stroke="#9aa4bf" />
              <YAxis stroke="#9aa4bf" />
              <Tooltip contentStyle={{ backgroundColor: '#1b2333', border: 'none' }} />
              <Legend />
              <Line type="monotone" dataKey="macd" stroke="#00bcd4" name="MACD" />
              <Line type="monotone" dataKey="signal" stroke="#ff9800" name="Signal" />
              <Area type="monotone" dataKey="histogram" fill="#4caf50" stroke="#388e3c" name="Histogram" />
            </AreaChart>
          )}
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default ChartPanel;
