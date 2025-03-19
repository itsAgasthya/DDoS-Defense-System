import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import debounce from 'lodash/debounce';

interface MonitoringData {
  is_active: boolean;
  uptime: string;
  packets_processed: number;
  packets_per_second: number;
  threat_level: string;
  recent_alerts: Array<{
    type: string;
    message: string;
    timestamp: string;
  }>;
  attack_statistics: {
    total_attacks: number;
    attack_types: Record<string, number>;
    mitigation_actions: {
      blocks_applied: number;
      rate_limits_activated: number;
      traffic_shaped: number;
    };
  };
  blockchain_status?: {
    connected: boolean;
    last_block: number;
    transactions_processed: number;
    attack_records: number;
  };
  predictive_analysis: {
    predicted_threat_level: string;
    confidence_score: number;
    trend_analysis: {
      packet_rate_trend: string;
      attack_probability: number;
    };
  };
  adaptive_response_status: {
    enabled: boolean;
    current_strategy: string;
    effectiveness: number;
    active_mitigations: number;
  };
}

interface AlertThresholds {
  critical: number;
  high: number;
  medium: number;
}

interface AdaptiveResponseConfig {
  enabled: boolean;
  auto_block: boolean;
  rate_limiting: boolean;
  traffic_shaping: boolean;
  mitigation_strategy: string;
}

interface AttackTypes {
  [key: string]: string;
}

interface ApiContextType {
  monitoringData: MonitoringData | null;
  isLoading: boolean;
  error: string | null;
  startMonitoring: () => Promise<void>;
  stopMonitoring: () => Promise<void>;
  updateAlertThresholds: (thresholds: AlertThresholds) => Promise<void>;
  updateAdaptiveResponse: (config: AdaptiveResponseConfig) => Promise<void>;
  getAttackTypes: () => Promise<AttackTypes>;
  getBlockchainStatus: () => Promise<any>;
  getPredictiveAnalysis: () => Promise<any>;
  getAdaptiveResponseStatus: () => Promise<any>;
}

const ApiContext = createContext<ApiContextType | undefined>(undefined);

export const useApi = () => {
  const context = useContext(ApiContext);
  if (!context) {
    throw new Error('useApi must be used within an ApiProvider');
  }
  return context;
};

export const ApiProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [monitoringData, setMonitoringData] = useState<MonitoringData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isMonitoring, setIsMonitoring] = useState(false);

  const API_BASE_URL = 'http://localhost:8000';

  const fetchMonitoringStatus = useCallback(async () => {
    if (!isMonitoring) return;
    
    try {
      const response = await axios.get(`${API_BASE_URL}/monitoring/status`);
      setMonitoringData(response.data);
    } catch (err) {
      setError('Failed to fetch monitoring status');
      console.error('Error fetching monitoring status:', err);
    }
  }, [isMonitoring, API_BASE_URL]);

  useEffect(() => {
    if (isMonitoring) {
      fetchMonitoringStatus();
      const interval = setInterval(fetchMonitoringStatus, 5000);
      return () => clearInterval(interval);
    }
  }, [isMonitoring, fetchMonitoringStatus]);

  const startMonitoring = async () => {
    try {
      setIsLoading(true);
      setError(null);
      await axios.post(`${API_BASE_URL}/monitoring/start`);
      setIsMonitoring(true);
    } catch (err) {
      setError('Failed to start monitoring');
      console.error('Error starting monitoring:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const stopMonitoring = async () => {
    try {
      setIsLoading(true);
      setError(null);
      await axios.post(`${API_BASE_URL}/monitoring/stop`);
      setIsMonitoring(false);
      setMonitoringData(null);
    } catch (err) {
      setError('Failed to stop monitoring');
      console.error('Error stopping monitoring:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const updateAlertThresholds = async (thresholds: AlertThresholds) => {
    try {
      setIsLoading(true);
      setError(null);
      await axios.post(`${API_BASE_URL}/monitoring/alert-thresholds`, thresholds);
    } catch (err) {
      setError('Failed to update alert thresholds');
      console.error('Error updating alert thresholds:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const updateAdaptiveResponse = async (config: AdaptiveResponseConfig) => {
    try {
      setIsLoading(true);
      setError(null);
      await axios.post(`${API_BASE_URL}/monitoring/adaptive-response`, config);
    } catch (err) {
      setError('Failed to update adaptive response configuration');
      console.error('Error updating adaptive response:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const getAttackTypes = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/monitoring/attack-types`);
      return response.data.attack_types;
    } catch (err) {
      setError('Failed to fetch attack types');
      console.error('Error fetching attack types:', err);
      return {};
    }
  };

  const getBlockchainStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/monitoring/blockchain/status`);
      return response.data;
    } catch (err) {
      setError('Failed to fetch blockchain status');
      console.error('Error fetching blockchain status:', err);
      return null;
    }
  };

  const getPredictiveAnalysis = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/monitoring/predictive-analysis`);
      return response.data;
    } catch (err) {
      setError('Failed to fetch predictive analysis');
      console.error('Error fetching predictive analysis:', err);
      return null;
    }
  };

  const getAdaptiveResponseStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/monitoring/adaptive-response/status`);
      return response.data;
    } catch (err) {
      setError('Failed to fetch adaptive response status');
      console.error('Error fetching adaptive response status:', err);
      return null;
    }
  };

  return (
    <ApiContext.Provider
      value={{
        monitoringData,
        isLoading,
        error,
        startMonitoring,
        stopMonitoring,
        updateAlertThresholds,
        updateAdaptiveResponse,
        getAttackTypes,
        getBlockchainStatus,
        getPredictiveAnalysis,
        getAdaptiveResponseStatus,
      }}
    >
      {children}
    </ApiContext.Provider>
  );
}; 