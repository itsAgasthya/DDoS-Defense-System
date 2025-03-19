import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Alert,
  Switch,
  FormControlLabel,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Slider,
} from '@mui/material';
import { useApi } from '../contexts/ApiContext';

const Settings: React.FC = () => {
  const { updateAlertThresholds, updateAdaptiveResponse } = useApi();
  const [alertThresholds, setAlertThresholds] = useState({
    critical: 1000,
    high: 750,
    medium: 500,
  });
  const [adaptiveConfig, setAdaptiveConfig] = useState({
    enabled: true,
    auto_block: true,
    rate_limiting: true,
    traffic_shaping: true,
    mitigation_strategy: 'adaptive',
  });
  const [status, setStatus] = useState<{
    type: 'success' | 'error' | 'info';
    message: string;
  } | null>(null);

  const handleThresholdsSubmit = async () => {
    try {
      await updateAlertThresholds(alertThresholds);
      setStatus({
        type: 'success',
        message: 'Alert thresholds updated successfully',
      });
    } catch (error) {
      setStatus({
        type: 'error',
        message: 'Failed to update alert thresholds',
      });
    }
  };

  const handleAdaptiveConfigSubmit = async () => {
    try {
      await updateAdaptiveResponse(adaptiveConfig);
      setStatus({
        type: 'success',
        message: 'Adaptive response configuration updated successfully',
      });
    } catch (error) {
      setStatus({
        type: 'error',
        message: 'Failed to update adaptive response configuration',
      });
    }
  };

  return (
    <Box p={3}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Alert Thresholds
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  label="Critical Threshold"
                  type="number"
                  value={alertThresholds.critical}
                  onChange={(e) =>
                    setAlertThresholds({
                      ...alertThresholds,
                      critical: parseInt(e.target.value),
                    })
                  }
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  label="High Threshold"
                  type="number"
                  value={alertThresholds.high}
                  onChange={(e) =>
                    setAlertThresholds({
                      ...alertThresholds,
                      high: parseInt(e.target.value),
                    })
                  }
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  label="Medium Threshold"
                  type="number"
                  value={alertThresholds.medium}
                  onChange={(e) =>
                    setAlertThresholds({
                      ...alertThresholds,
                      medium: parseInt(e.target.value),
                    })
                  }
                />
              </Grid>
              <Grid item xs={12}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleThresholdsSubmit}
                >
                  Update Thresholds
                </Button>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Adaptive Response Configuration
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={adaptiveConfig.enabled}
                      onChange={(e) =>
                        setAdaptiveConfig({
                          ...adaptiveConfig,
                          enabled: e.target.checked,
                        })
                      }
                    />
                  }
                  label="Enable Adaptive Response"
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={adaptiveConfig.auto_block}
                      onChange={(e) =>
                        setAdaptiveConfig({
                          ...adaptiveConfig,
                          auto_block: e.target.checked,
                        })
                      }
                    />
                  }
                  label="Enable Automatic Blocking"
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={adaptiveConfig.rate_limiting}
                      onChange={(e) =>
                        setAdaptiveConfig({
                          ...adaptiveConfig,
                          rate_limiting: e.target.checked,
                        })
                      }
                    />
                  }
                  label="Enable Rate Limiting"
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={adaptiveConfig.traffic_shaping}
                      onChange={(e) =>
                        setAdaptiveConfig({
                          ...adaptiveConfig,
                          traffic_shaping: e.target.checked,
                        })
                      }
                    />
                  }
                  label="Enable Traffic Shaping"
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Mitigation Strategy</InputLabel>
                  <Select
                    value={adaptiveConfig.mitigation_strategy}
                    onChange={(e) =>
                      setAdaptiveConfig({
                        ...adaptiveConfig,
                        mitigation_strategy: e.target.value as string,
                      })
                    }
                  >
                    <MenuItem value="adaptive">Adaptive</MenuItem>
                    <MenuItem value="aggressive">Aggressive</MenuItem>
                    <MenuItem value="conservative">Conservative</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleAdaptiveConfigSubmit}
                >
                  Update Adaptive Response
                </Button>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Blockchain Configuration
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <FormControlLabel
                  control={<Switch defaultChecked />}
                  label="Enable Blockchain Integration"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Smart Contract Address"
                  defaultValue="0x..."
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={<Switch defaultChecked />}
                  label="Record Attack Events"
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={<Switch defaultChecked />}
                  label="Enable Attack Pattern Sharing"
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Predictive Analysis Settings
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <FormControlLabel
                  control={<Switch defaultChecked />}
                  label="Enable Predictive Analysis"
                />
              </Grid>
              <Grid item xs={12}>
                <Typography gutterBottom>Confidence Threshold</Typography>
                <Slider
                  defaultValue={0.8}
                  min={0}
                  max={1}
                  step={0.1}
                  marks
                  valueLabelDisplay="auto"
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={<Switch defaultChecked />}
                  label="Enable Trend Analysis"
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={<Switch defaultChecked />}
                  label="Enable Attack Pattern Recognition"
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>

      {status && (
        <Box mt={2}>
          <Alert severity={status.type}>{status.message}</Alert>
        </Box>
      )}
    </Box>
  );
};

export default Settings; 