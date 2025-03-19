import React from 'react';
import { Box, Paper, Typography, Button } from '@mui/material';
import { useApi } from '../contexts/ApiContext';

export default function Monitoring() {
  const { startMonitoring, stopMonitoring } = useApi();

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Traffic Monitoring
        </Typography>
        <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => startMonitoring()}
          >
            Start Monitoring
          </Button>
          <Button
            variant="contained"
            color="secondary"
            onClick={() => stopMonitoring()}
          >
            Stop Monitoring
          </Button>
        </Box>
      </Paper>
    </Box>
  );
} 