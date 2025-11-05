import { useState } from 'react';
import { Box, Container, Grid, Paper } from '@mui/material';
import SearchBar from './components/SearchBar';
import OverviewPanel from './components/OverviewPanel';
import FinancialPanel from './components/FinancialPanel';
import ChartPanel from './components/ChartPanel';
import NewsPanel from './components/NewsPanel';
import InsightsPanel from './components/InsightsPanel';
import ComparisonPanel from './components/ComparisonPanel';
import EventStreamPanel from './components/EventStreamPanel';
import { useDashboardData } from './hooks/useDashboardData';

function App() {
  const [symbol, setSymbol] = useState('AAPL');
  const { data, loading } = useDashboardData(symbol);

  return (
    <Box sx={{ minHeight: '100vh', background: 'radial-gradient(circle at top left, #15213b 0%, #05070f 60%)' }}>
      <Container maxWidth={false} sx={{ paddingY: 4 }}>
        <SearchBar onSelect={setSymbol} activeSymbol={symbol} />
        <Grid container spacing={2} sx={{ marginTop: 1 }}>
          <Grid item xs={12} md={4}>
            <OverviewPanel data={data} loading={loading} />
            <EventStreamPanel />
          </Grid>
          <Grid item xs={12} md={8}>
            <ChartPanel data={data} loading={loading} />
          </Grid>
          <Grid item xs={12} md={6}>
            <FinancialPanel data={data} loading={loading} />
          </Grid>
          <Grid item xs={12} md={6}>
            <InsightsPanel data={data} loading={loading} />
          </Grid>
          <Grid item xs={12} md={7}>
            <NewsPanel data={data} loading={loading} />
          </Grid>
          <Grid item xs={12} md={5}>
            <ComparisonPanel symbol={symbol} />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App;
