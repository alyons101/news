import { useEffect, useState } from 'react';
import { Card, CardContent, CircularProgress, Divider, Stack, TextField, Typography } from '@mui/material';
import { fetchComparison } from '../services/api';

interface Props {
  symbol: string;
}

const ComparisonPanel = ({ symbol }: Props) => {
  const [symbols, setSymbols] = useState<string>(`${symbol},MSFT`);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    setSymbols(`${symbol},MSFT`);
  }, [symbol]);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const tokens = symbols.split(',').map((s) => s.trim().toUpperCase()).filter(Boolean);
      const result = await fetchComparison(tokens);
      setData(result);
      setLoading(false);
    };
    load();
  }, [symbols]);

  return (
    <Card sx={{ backgroundColor: 'rgba(20,24,38,0.85)', height: 320 }}>
      <CardContent>
        <Stack spacing={2}>
          <Typography variant="h6">Comparisons</Typography>
          <TextField
            label="Symbols"
            value={symbols}
            onChange={(event) => setSymbols(event.target.value)}
            helperText="Comma separated tickers"
          />
          {loading && <CircularProgress size={24} />}
          {!loading && data && (
            <Stack spacing={1}>
              {data.ratios.map((row: any) => (
                <Stack key={row.symbol} spacing={0.5}>
                  <Typography variant="subtitle2">{row.symbol}</Typography>
                  <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                    EPS {row.valuation.eps.toFixed(2)} · Net Margin {row.profitability.netMargin.toFixed(2)}% · ROE {row.leverage.returnOnEquity.toFixed(2)}
                  </Typography>
                </Stack>
              ))}
              <Divider sx={{ borderColor: 'rgba(255,255,255,0.05)' }} />
              <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                Correlation matrix ready for download: {JSON.stringify(data.correlations.matrix)}
              </Typography>
            </Stack>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
};

export default ComparisonPanel;
