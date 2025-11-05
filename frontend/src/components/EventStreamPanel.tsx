import { useEffect, useRef, useState } from 'react';
import { Alert, Card, CardContent, Stack, Typography } from '@mui/material';

interface EventMessage {
  type: string;
  category?: string;
  message?: string;
  payload?: {
    title: string;
    detail: string;
    severity: 'low' | 'medium' | 'high';
  };
}

const severityMapping: Record<string, 'success' | 'info' | 'warning' | 'error'> = {
  low: 'info',
  medium: 'warning',
  high: 'error'
};

const EventStreamPanel = () => {
  const [events, setEvents] = useState<EventMessage[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    try {
      const ws = new WebSocket('ws://localhost:8000/api/ws/events');
      wsRef.current = ws;
      ws.onmessage = (message) => {
        const data = JSON.parse(message.data);
        setEvents((prev) => [data, ...prev].slice(0, 4));
      };
      ws.onerror = () => {
        ws.close();
      };
    } catch (error) {
      console.warn('WebSocket connection failed', error);
    }
    return () => {
      wsRef.current?.close();
    };
  }, []);

  return (
    <Card sx={{ backgroundColor: 'rgba(20,24,38,0.85)', marginTop: 2 }}>
      <CardContent>
        <Typography variant="subtitle1" gutterBottom>Live Events</Typography>
        <Stack spacing={1}>
          {events.map((event, index) => (
            <Alert
              key={index}
              severity={severityMapping[event.payload?.severity ?? 'low']}
              sx={{ backgroundColor: 'rgba(0,188,212,0.1)', borderColor: 'rgba(0,188,212,0.3)' }}
            >
              <Typography variant="body2" fontWeight={600}>{event.payload?.title ?? event.message}</Typography>
              <Typography variant="caption">{event.payload?.detail}</Typography>
            </Alert>
          ))}
          {!events.length && <Typography variant="caption" color="text.secondary">Awaiting macro events...</Typography>}
        </Stack>
      </CardContent>
    </Card>
  );
};

export default EventStreamPanel;
