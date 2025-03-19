import React from 'react';
import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Grid,
  LinearProgress,
  Divider,
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,
  Analytics as AnalyticsIcon,
  AutoFixHigh as AdaptiveIcon,
  AccountBalance as BlockchainIcon,
} from '@mui/icons-material';

interface Model {
  name: string;
  description: string;
  status: 'active' | 'inactive' | 'training';
  type: 'detection' | 'prediction' | 'classification' | 'adaptive' | 'blockchain';
  accuracy: number;
  features: string[];
}

const models: Model[] = [
  {
    name: 'Isolation Forest',
    description: 'Anomaly detection model for identifying unusual traffic patterns',
    status: 'active',
    type: 'detection',
    accuracy: 0.95,
    features: ['Real-time detection', 'Low false positive rate', 'Adaptive thresholds'],
  },
  {
    name: 'LSTM Neural Network',
    description: 'Predictive model for forecasting potential DDoS attacks',
    status: 'active',
    type: 'prediction',
    accuracy: 0.88,
    features: ['Time-series analysis', 'Pattern recognition', 'Early warning system'],
  },
  {
    name: 'Random Forest Classifier',
    description: 'Multi-class classification model for identifying attack types',
    status: 'active',
    type: 'classification',
    accuracy: 0.92,
    features: ['Attack type classification', 'Feature importance analysis', 'High accuracy'],
  },
  {
    name: 'Adaptive Response System',
    description: 'Dynamic mitigation system that adjusts to attack patterns',
    status: 'active',
    type: 'adaptive',
    accuracy: 0.85,
    features: ['Real-time adaptation', 'Multiple mitigation strategies', 'Performance optimization'],
  },
  {
    name: 'Blockchain Validator',
    description: 'Blockchain-based attack pattern sharing and validation',
    status: 'active',
    type: 'blockchain',
    accuracy: 1.0,
    features: ['Immutable records', 'Pattern sharing', 'Consensus validation'],
  },
];

const getStatusColor = (status: Model['status']) => {
  switch (status) {
    case 'active':
      return 'success';
    case 'inactive':
      return 'error';
    case 'training':
      return 'warning';
    default:
      return 'default';
  }
};

const getTypeIcon = (type: Model['type']) => {
  switch (type) {
    case 'detection':
      return <SecurityIcon />;
    case 'prediction':
      return <AnalyticsIcon />;
    case 'classification':
      return <CheckCircleIcon />;
    case 'adaptive':
      return <AdaptiveIcon />;
    case 'blockchain':
      return <BlockchainIcon />;
    default:
      return <WarningIcon />;
  }
};

const Models: React.FC = () => {
  return (
    <Box p={3}>
      <Grid container spacing={3}>
        {models.map((model) => (
          <Grid item xs={12} md={6} key={model.name}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Box display="flex" alignItems="center" mb={2}>
                <Box mr={2}>{getTypeIcon(model.type)}</Box>
                <Typography variant="h6">{model.name}</Typography>
                <Box ml="auto">
                  <Chip
                    label={model.status}
                    color={getStatusColor(model.status)}
                    size="small"
                  />
                </Box>
              </Box>
              <Typography color="textSecondary" paragraph>
                {model.description}
              </Typography>
              <Box mb={2}>
                <Typography variant="subtitle2" gutterBottom>
                  Accuracy: {(model.accuracy * 100).toFixed(1)}%
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={model.accuracy * 100}
                  color={model.accuracy > 0.9 ? 'success' : 'primary'}
                />
              </Box>
              <Divider sx={{ my: 2 }} />
              <Typography variant="subtitle2" gutterBottom>
                Features:
              </Typography>
              <List dense>
                {model.features.map((feature) => (
                  <ListItem key={feature}>
                    <ListItemIcon>
                      <CheckCircleIcon color="success" fontSize="small" />
                    </ListItemIcon>
                    <ListItemText primary={feature} />
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Models; 