import { Card, CardContent, CircularProgress, Typography } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

interface Props {
  data: any;
  loading: boolean;
}

const columns: GridColDef[] = [
  { field: 'year', headerName: 'Year', flex: 1 },
  { field: 'revenue', headerName: 'Revenue ($M)', flex: 1, valueFormatter: ({ value }) => value.toLocaleString() },
  { field: 'netIncome', headerName: 'Net Income ($M)', flex: 1, valueFormatter: ({ value }) => value.toLocaleString() },
  { field: 'eps', headerName: 'EPS', flex: 0.6 }
];

const FinancialPanel = ({ data, loading }: Props) => {
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
        <Typography variant="h6" gutterBottom>Financials</Typography>
        <DataGrid
          sx={{ height: 250, border: 'none', color: 'white' }}
          rows={data.incomeStatement.map((row: any, index: number) => ({ id: index, ...row }))}
          columns={columns}
          hideFooter
        />
      </CardContent>
    </Card>
  );
};

export default FinancialPanel;
