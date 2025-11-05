import { Card, CardContent, CircularProgress, Stack, Typography } from '@mui/material';
import EmojiObjectsIcon from '@mui/icons-material/EmojiObjects';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import TimelineIcon from '@mui/icons-material/Timeline';

interface Props {
  data: any;
  loading: boolean;
}

const InsightsPanel = ({ data, loading }: Props) => {
  if (loading || !data) {
    return (
      <Card sx={{ backgroundColor: 'rgba(20,24,38,0.85)', height: 320 }}>
        <CardContent sx={{ display: 'flex', justifyContent: 'center' }}>
          <CircularProgress size={28} />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ backgroundColor: 'rgba(20,24,38,0.85)', height: 320 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>AI & Quant Insights</Typography>
        <Stack spacing={2}>
          <Stack direction="row" spacing={2}>
            <EmojiObjectsIcon color="primary" />
            <Typography variant="body2">{data.aiSummary.summary}</Typography>
          </Stack>
          <Stack direction="row" spacing={2}>
            <ShowChartIcon color="primary" />
            <Typography variant="body2">
              Predictive trend suggests an {data.predictive?.trend ?? 'unknown'} with
              {' '}
              {Math.round((data.predictive?.confidence ?? 0) * 100)}% confidence.
              {' '}
              Projected price: ${data.predictive?.projectedPrice ? data.predictive.projectedPrice.toFixed(2) : 'N/A'}
            </Typography>
          </Stack>
          <Stack direction="row" spacing={2}>
            <TimelineIcon color="primary" />
            <Typography variant="body2">
              Annualized volatility {Math.round((data.volatility?.volatility ?? 0) * 100)}%. Anomaly count:
              {' '}
              {data.anomalies?.anomalies?.length ?? 0}
            </Typography>
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default InsightsPanel;
