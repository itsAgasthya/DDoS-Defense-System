import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
} from '@mui/material';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
} from '@mui/lab';
import {
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Block as BlockIcon,
  Speed as SpeedIcon,
  Security as SecurityIcon,
  AccountTree as BlockchainIcon,
  Analytics as AnalyticsIcon,
  AutoFixHigh as AdaptiveIcon,
} from '@mui/icons-material';
import { useApi } from '../contexts/ApiContext';

// Utility function to format numbers
const formatNumber = (num: number) => {
  return new Intl.NumberFormat().format(num);
};

// Utility function to format time duration
const formatDuration = (duration: string) => {
  return duration;
};

const StatCard: React.FC<{
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color?: string;
}> = ({ title, value, icon, color }) => (
  <Paper sx={{ p: 2, height: '100%' }}>
    <Box display="flex" alignItems="center" justifyContent="space-between">
      <Box>
        <Typography variant="subtitle2" color="textSecondary">
          {title}
        </Typography>
        <Typography variant="h4">{value}</Typography>
      </Box>
      <Box
        sx={{
          backgroundColor: color || 'primary.main',
          borderRadius: '50%',
          p: 1,
          display: 'flex',
        }}
      >
        {icon}
      </Box>
    </Box>
  </Paper>
);

const ThreatLevelIndicator: React.FC<{ level: string }> = ({ level }) => {
  const getColor = () => {
    switch (level) {
      case 'CRITICAL':
        return 'error';
      case 'HIGH':
        return 'warning';
      case 'MEDIUM':
        return 'info';
      default:
        return 'success';
    }
  };

  return (
    <Paper sx={{ p: 2, height: '100%' }}>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Box>
          <Typography variant="subtitle2" color="textSecondary">
            Current Threat Level
          </Typography>
          <Typography variant="h4" color={`${getColor()}.main`}>
            {level}
          </Typography>
        </Box>
        <WarningIcon color={getColor()} sx={{ fontSize: 40 }} />
      </Box>
    </Paper>
  );
};

const AttackStatistics: React.FC<{
  stats: {
    total_attacks: number;
    attack_types: Record<string, number>;
    mitigation_actions: {
      blocks_applied: number;
      rate_limits_activated: number;
      traffic_shaped: number;
    };
  };
}> = ({ stats }) => (
  <Paper sx={{ p: 2, height: '100%' }}>
    <Typography variant="h6" gutterBottom>
      Attack Statistics
    </Typography>
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="subtitle1">
          Total Attacks: {stats.total_attacks}
        </Typography>
      </Grid>
      <Grid item xs={12}>
        <Typography variant="subtitle2" gutterBottom>
          Attack Types:
        </Typography>
        <Box display="flex" flexWrap="wrap" gap={1}>
          {Object.entries(stats.attack_types).map(([type, count]) => (
            <Chip
              key={type}
              label={`${type}: ${count}`}
              color="primary"
              variant="outlined"
            />
          ))}
        </Box>
      </Grid>
      <Grid item xs={12}>
        <Typography variant="subtitle2" gutterBottom>
          Mitigation Actions:
        </Typography>
        <List dense>
          <ListItem>
            <ListItemIcon>
              <BlockIcon color="error" />
            </ListItemIcon>
            <ListItemText
              primary={`Blocks Applied: ${stats.mitigation_actions.blocks_applied}`}
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <SpeedIcon color="warning" />
            </ListItemIcon>
            <ListItemText
              primary={`Rate Limits Activated: ${stats.mitigation_actions.rate_limits_activated}`}
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <SecurityIcon color="info" />
            </ListItemIcon>
            <ListItemText
              primary={`Traffic Shaped: ${stats.mitigation_actions.traffic_shaped}`}
            />
          </ListItem>
        </List>
      </Grid>
    </Grid>
  </Paper>
);

interface BlockchainStatusProps {
  status: {
    connected: boolean;
    last_block: number;
    transactions_processed: number;
    attack_records: number;
  } | null;
}

const BlockchainStatus: React.FC<BlockchainStatusProps> = ({ status }) => {
  if (!status) return null;
  
  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        <BlockchainIcon sx={{ mr: 1 }} />
        Blockchain Status
      </Typography>
      <List>
        <ListItem>
          <ListItemIcon>
            <BlockchainIcon color={status.connected ? "success" : "error"} />
          </ListItemIcon>
          <ListItemText 
            primary="Connection Status" 
            secondary={status.connected ? "Connected" : "Disconnected"} 
          />
        </ListItem>
        <ListItem>
          <ListItemText 
            primary="Last Block" 
            secondary={status.last_block} 
          />
        </ListItem>
        <ListItem>
          <ListItemText 
            primary="Transactions Processed" 
            secondary={status.transactions_processed} 
          />
        </ListItem>
        <ListItem>
          <ListItemText 
            primary="Attack Records" 
            secondary={status.attack_records} 
          />
        </ListItem>
      </List>
    </Paper>
  );
};

const PredictiveAnalysis: React.FC<{
  analysis: {
    predicted_threat_level: string;
    confidence_score: number;
    trend_analysis: {
      packet_rate_trend: string;
      attack_probability: number;
    };
  };
}> = ({ analysis }) => (
  <Paper sx={{ p: 2, height: '100%' }}>
    <Typography variant="h6" gutterBottom>
      Predictive Analysis
    </Typography>
    <List dense>
      <ListItem>
        <ListItemIcon>
          <AnalyticsIcon color="primary" />
        </ListItemIcon>
        <ListItemText
          primary={`Predicted Threat Level: ${analysis.predicted_threat_level}`}
        />
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <AnalyticsIcon color="primary" />
        </ListItemIcon>
        <ListItemText
          primary={`Confidence Score: ${(analysis.confidence_score * 100).toFixed(1)}%`}
        />
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <AnalyticsIcon color="primary" />
        </ListItemIcon>
        <ListItemText
          primary={`Packet Rate Trend: ${analysis.trend_analysis.packet_rate_trend}`}
        />
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <AnalyticsIcon color="primary" />
        </ListItemIcon>
        <ListItemText
          primary={`Attack Probability: ${(analysis.trend_analysis.attack_probability * 100).toFixed(1)}%`}
        />
      </ListItem>
    </List>
  </Paper>
);

const AdaptiveResponse: React.FC<{
  status: {
    enabled: boolean;
    current_strategy: string;
    effectiveness: number;
    active_mitigations: number;
  };
}> = ({ status }) => (
  <Paper sx={{ p: 2, height: '100%' }}>
    <Typography variant="h6" gutterBottom>
      Adaptive Response
    </Typography>
    <List dense>
      <ListItem>
        <ListItemIcon>
          <AdaptiveIcon color={status.enabled ? 'success' : 'error'} />
        </ListItemIcon>
        <ListItemText
          primary={`Status: ${status.enabled ? 'Enabled' : 'Disabled'}`}
        />
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <AdaptiveIcon color="primary" />
        </ListItemIcon>
        <ListItemText
          primary={`Current Strategy: ${status.current_strategy}`}
        />
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <AdaptiveIcon color="primary" />
        </ListItemIcon>
        <ListItemText
          primary={`Effectiveness: ${(status.effectiveness * 100).toFixed(1)}%`}
        />
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <AdaptiveIcon color="primary" />
        </ListItemIcon>
        <ListItemText
          primary={`Active Mitigations: ${status.active_mitigations}`}
        />
      </ListItem>
    </List>
  </Paper>
);

const RecentAlerts: React.FC<{ alerts: any[] }> = ({ alerts }) => (
  <Paper sx={{ p: 2, height: '100%' }}>
    <Typography variant="h6" gutterBottom>
      Recent Alerts
    </Typography>
    <Timeline>
      {alerts.map((alert, index) => (
        <TimelineItem key={index}>
          <TimelineSeparator>
            <TimelineDot color="error" />
            {index < alerts.length - 1 && <TimelineConnector />}
          </TimelineSeparator>
          <TimelineContent>
            <Typography variant="subtitle2">{alert.type}</Typography>
            <Typography variant="body2" color="textSecondary">
              {alert.message}
            </Typography>
            <Typography variant="caption" color="textSecondary">
              {new Date(alert.timestamp).toLocaleString()}
            </Typography>
          </TimelineContent>
        </TimelineItem>
      ))}
    </Timeline>
  </Paper>
);

const Dashboard: React.FC = () => {
  const { monitoringData, isLoading, error, startMonitoring } = useApi();

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={2}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  if (!monitoringData) {
    return (
      <Box p={2}>
        <Alert severity="info">Start monitoring to view dashboard data</Alert>
      </Box>
    );
  }

  return (
    <Box p={2}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <ThreatLevelIndicator level={monitoringData.threat_level} />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Packets Processed"
            value={formatNumber(monitoringData.packets_processed)}
            icon={<CheckCircleIcon sx={{ color: 'white' }} />}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Packets/Second"
            value={formatNumber(monitoringData.packets_per_second)}
            icon={<SpeedIcon sx={{ color: 'white' }} />}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Uptime"
            value={formatDuration(monitoringData.uptime)}
            icon={<CheckCircleIcon sx={{ color: 'white' }} />}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <AttackStatistics stats={monitoringData.attack_statistics} />
        </Grid>
        <Grid item xs={12} md={6}>
          <BlockchainStatus status={monitoringData.blockchain_status || null} />
        </Grid>
        <Grid item xs={12} md={6}>
          <PredictiveAnalysis analysis={monitoringData.predictive_analysis} />
        </Grid>
        <Grid item xs={12} md={6}>
          <AdaptiveResponse status={monitoringData.adaptive_response_status} />
        </Grid>
        <Grid item xs={12}>
          <RecentAlerts alerts={monitoringData.recent_alerts} />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 