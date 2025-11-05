import { useEffect, useState } from 'react';
import { Autocomplete, Box, TextField, Typography } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { fetchSearch } from '../services/api';

interface SearchResult {
  symbol: string;
  name: string;
  sector: string;
  industry: string;
}

interface Props {
  onSelect: (symbol: string) => void;
  activeSymbol: string;
}

const SearchBar = ({ onSelect, activeSymbol }: Props) => {
  const [query, setQuery] = useState(activeSymbol);
  const [options, setOptions] = useState<SearchResult[]>([]);

  useEffect(() => {
    if (!query) {
      setOptions([]);
      return;
    }
    const handler = setTimeout(async () => {
      const results = await fetchSearch(query);
      setOptions(results);
    }, 250);
    return () => clearTimeout(handler);
  }, [query]);

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', backgroundColor: 'rgba(20,24,38,0.85)', borderRadius: 2, padding: 2 }}>
      <SearchIcon sx={{ marginRight: 2, color: 'primary.main' }} />
      <Autocomplete
        sx={{ flex: 1 }}
        options={options}
        getOptionLabel={(option) => `${option.symbol} · ${option.name}`}
        onInputChange={(_, value) => setQuery(value)}
        onChange={(_, value) => value && onSelect(value.symbol)}
        renderInput={(params) => <TextField {...params} variant="standard" label="Search companies, tickers, themes" />}
      />
      <Typography variant="body2" sx={{ marginLeft: 2, color: 'text.secondary' }}>
        Try: "Compare Apple and Microsoft"
      </Typography>
    </Box>
  );
};

export default SearchBar;
