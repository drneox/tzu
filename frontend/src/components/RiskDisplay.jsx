import React from 'react';
import { Badge, VStack, Text, Box } from '@chakra-ui/react';
import { getRiskColorScheme, getRiskColorCSS, getRiskLabel } from '../utils/riskCalculations';
import { useLocalization } from '../hooks/useLocalization';

/**
 * Component to display risk values consistently across the application
 */
const RiskDisplay = ({ 
  riskValue = 0, 
  label = 'Risk', 
  size = 'md', 
  showLabel = true,
  variant = 'badge', // 'badge' or 'box'
  prefix = null // For compact display like 'IR: 4.5'
}) => {
  const { t } = useLocalization();
  
  const formattedValue = parseFloat(riskValue || 0).toFixed(1);
  const colorScheme = getRiskColorScheme(riskValue);
  const riskLevelLabel = getRiskLabel(riskValue, t);

  if (variant === 'box') {
    const riskDisplayStyles = {
      container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '8px',
        borderRadius: '8px',
        minWidth: '80px',
        backgroundColor: '#f7fafc'
      },
      numberValue: {
        fontSize: size === 'sm' ? '18px' : '24px',
        fontWeight: 'bold',
        lineHeight: '1.2',
        marginBottom: '4px'
      },
      riskLabel: {
        fontSize: '10px',
        fontWeight: 'bold',
        color: 'white',
        padding: '2px 8px',
        borderRadius: '12px',
        textTransform: 'uppercase',
        letterSpacing: '0.5px'
      }
    };

    const roundedValue = Math.round(riskValue * 2) / 2;
    const riskColor = getRiskColorCSS(roundedValue);

    return (
      <div style={riskDisplayStyles.container}>
        {showLabel && (
          <Text fontSize="xs" color="gray.600" mb={1}>
            {label}
          </Text>
        )}
        <div style={{
          ...riskDisplayStyles.numberValue,
          color: riskColor
        }}>
          {formattedValue}
        </div>
        <div style={{
          ...riskDisplayStyles.riskLabel,
          backgroundColor: riskColor
        }}>
          {riskLevelLabel}
        </div>
      </div>
    );
  }

  return (
    <VStack spacing={1} align="center">
      {showLabel && !prefix && (
        <Text fontSize="xs" color="gray.600">
          {label}
        </Text>
      )}
      <Badge 
        colorScheme={colorScheme} 
        fontSize={size === 'sm' ? 'xs' : 'sm'}
        px={2}
        py={1}
      >
        {prefix ? `${prefix}: ${formattedValue}` : `${formattedValue} (${riskLevelLabel})`}
      </Badge>
    </VStack>
  );
};

export default RiskDisplay;
