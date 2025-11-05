import { Card, CardContent, Chip, CircularProgress, Divider, Stack, Typography } from '@mui/material';

interface Props {
  data: any;
  loading: boolean;
}

const sentimentColor = (score: number) => {
  if (score > 0.2) return 'success';
  if (score < -0.2) return 'error';
  return 'default';
};

const NewsPanel = ({ data, loading }: Props) => {
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
    <Card sx={{ backgroundColor: 'rgba(20,24,38,0.85)', height: 320, overflowY: 'auto' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>News & Media</Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', marginBottom: 1 }}>
          Sentiment score: {data.sentiment.sentiment.toFixed(2)}
        </Typography>
        {data.news.map((item: any, index: number) => (
          <Stack key={item.title} spacing={1} sx={{ marginBottom: 2 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
              <Typography variant="subtitle2">{item.title}</Typography>
              <Chip size="small" label={`${item.source}`} color={sentimentColor(item.sentiment)} />
            </Stack>
            <Typography variant="caption" sx={{ color: 'text.secondary' }}>{new Date(item.publishedAt).toLocaleString()}</Typography>
            <Typography variant="body2">{item.summary}</Typography>
            <iframe
              title={item.title}
              src={item.videoUrl}
              style={{ border: 'none', borderRadius: 8, height: 160 }}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
            {index < data.news.length - 1 && <Divider sx={{ borderColor: 'rgba(255,255,255,0.05)' }} />}
          </Stack>
        ))}
      </CardContent>
    </Card>
  );
};

export default NewsPanel;
