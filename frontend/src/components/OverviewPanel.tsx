import { Card, CardContent, CircularProgress, Stack, Typography } from '@mui/material';
import CorporateFareIcon from '@mui/icons-material/CorporateFare';
import FactoryIcon from '@mui/icons-material/Factory';
import PublicIcon from '@mui/icons-material/Public';

interface Props {
  data: any;
  loading: boolean;
}

const OverviewPanel = ({ data, loading }: Props) => {
  if (loading || !data) {
    return (
      <Card sx={{ backgroundColor: 'rgba(20,24,38,0.85)' }}>
        <CardContent sx={{ display: 'flex', justifyContent: 'center' }}>
          <CircularProgress size={28} />
        </CardContent>
      </Card>
    );
  }

  const { company, ratios } = data;

  return (
    <Card sx={{ backgroundColor: 'rgba(20,24,38,0.85)', marginBottom: 2 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>{company.symbol} · {company.name}</Typography>
        <Stack spacing={1}>
          <Stack direction="row" spacing={1} alignItems="center">
            <CorporateFareIcon color="primary" />
            <Typography variant="body2">Sector: {company.sector}</Typography>
          </Stack>
          <Stack direction="row" spacing={1} alignItems="center">
            <FactoryIcon color="primary" />
            <Typography variant="body2">Industry: {company.industry}</Typography>
          </Stack>
          <Stack direction="row" spacing={1} alignItems="center">
            <PublicIcon color="primary" />
            <Typography variant="body2">Headquarters: {company.headquarters}</Typography>
          </Stack>
        </Stack>
        <Typography variant="body2" sx={{ marginTop: 2, color: 'text.secondary' }}>{company.description}</Typography>
        <Typography variant="subtitle2" sx={{ marginTop: 2 }}>ESG Score: {company.esgScore} · Market Cap ${(company.marketCap / 1e9).toFixed(1)}B</Typography>
        <Typography variant="caption" sx={{ color: 'text.secondary' }}>EPS: {ratios.valuation.eps.toFixed(2)} · Net Margin: {ratios.profitability.netMargin.toFixed(2)}%</Typography>
      </CardContent>
    </Card>
  );
};

export default OverviewPanel;
