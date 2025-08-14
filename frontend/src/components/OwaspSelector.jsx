import React from 'react';
import { getOwaspSelectOptions } from '../hooks/useLocalization';

const OwaspSelector = ({ 
  factorName, 
  threatId, 
  value = 0, 
  onChange, 
  locale = 'es',
  style = {} 
}) => {
  const options = getOwaspSelectOptions(factorName, locale) || [];
  
  const handleChange = (event) => {
    if (onChange) {
      onChange(threatId);
    }
  };

  return (
    <select
      value={value || 0}
      style={{ width: "100px", ...style }}
      id={`${factorName}-${threatId}`}
      onChange={handleChange}
    >
      {options.map(option => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
};

export default OwaspSelector;
