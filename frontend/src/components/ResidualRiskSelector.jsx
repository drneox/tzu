import React from 'react';
import { getRiskColorCSS, getRiskLabel } from '../utils/riskCalculations';
import { useLocalization } from '../hooks/useLocalization';

/**
 * ResidualRiskSelector - Component that combines risk display with editable selector
 */
const ResidualRiskSelector = ({ 
  threatId, 
  currentValue, 
  onUpdate,
  size = 'md'
}) => {
  const { t } = useLocalization();
  
  // Generate options from 0.5 to 9 in 0.5 increments
  const options = [];
  for (let i = 0.5; i <= 9; i += 0.5) {
    options.push(i);
  }
  
  const roundedValue = Math.round(currentValue * 2) / 2;
  const riskColor = getRiskColorCSS(roundedValue);
  const riskLabel = getRiskLabel(roundedValue, t);
  
  const riskDisplayStyles = {
    container: {
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '2px',
      width: '100%',
      cursor: 'pointer'
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
    },
    invisibleSelect: {
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      opacity: 0,
      cursor: 'pointer',
      zIndex: 10,
      appearance: 'none',
      background: 'transparent',
      border: 'none'
    },
    dropdownIcon: {
      position: 'absolute',
      top: '2px',
      right: '2px',
      fontSize: '8px',
      pointerEvents: 'none',
      zIndex: 5
    }
  };

  return (
    <div style={riskDisplayStyles.container}>
      {/* Visual Risk Display */}
      <div style={{
        ...riskDisplayStyles.numberValue,
        color: riskColor
      }}>
        {roundedValue.toFixed(1)}
      </div>
      
      <div style={{
        ...riskDisplayStyles.riskLabel,
        backgroundColor: riskColor
      }}>
        {riskLabel}
      </div>
      
      {/* Invisible Select Overlay */}
      <select 
        value={roundedValue}
        onChange={(e) => onUpdate(threatId, parseFloat(e.target.value))}
        style={riskDisplayStyles.invisibleSelect}
      >
        {options.map(value => (
          <option key={value} value={value}>
            {value.toFixed(1)} - {getRiskLabel(value, t)}
          </option>
        ))}
      </select>
      
      {/* Dropdown Icon */}
      <div style={{
        ...riskDisplayStyles.dropdownIcon,
        color: riskColor
      }}>
        ▼
      </div>
    </div>
  );
};

export default ResidualRiskSelector;
