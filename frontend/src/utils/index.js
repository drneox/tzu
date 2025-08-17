/**
 * Utility functions for the application
 */

/**
 * Format a date according to locale
 * @param {Date} date - The date to format
 * @param {string} locale - The locale to use for formatting
 * @returns {string} Formatted date string
 */
export const formatDate = (date, locale = 'es') => {
  if (!date || !(date instanceof Date) || isNaN(date.getTime())) {
    return date === null || date === undefined ? '' : 'Invalid Date';
  }
  
  try {
    return date.toLocaleDateString(locale === 'es' ? 'es-ES' : 'en-US');
  } catch (error) {
    return date.toLocaleDateString();
  }
};

/**
 * Format risk value to 2 decimal places
 * @param {number|string|null|undefined} riskValue - The risk value to format
 * @returns {string} Formatted risk value
 */
export const formatRisk = (riskValue) => {
  const numValue = parseFloat(riskValue);
  
  if (isNaN(numValue) || riskValue === null || riskValue === undefined) {
    return '0.00';
  }
  
  return numValue.toFixed(2);
};

/**
 * Generate a unique threat ID
 * @returns {string} Unique threat ID
 */
export const generateThreatId = () => {
  const timestamp = Date.now().toString(36);
  const randomPart = Math.random().toString(36).substring(2);
  return `threat_${timestamp}_${randomPart}`;
};

/**
 * Validate OWASP risk factors
 * @param {Object} riskFactors - The risk factors to validate
 * @returns {Object} Validation result with isValid flag and errors array
 */
export const validateRiskFactors = (riskFactors) => {
  const errors = [];
  
  if (!riskFactors || typeof riskFactors !== 'object') {
    return { isValid: false, errors: ['Risk factors object is required'] };
  }
  
  const requiredFactors = [
    'skill_level', 'motive', 'opportunity', 'size',
    'ease_of_discovery', 'ease_of_exploit', 'awareness', 'intrusion_detection',
    'loss_of_confidentiality', 'loss_of_integrity', 'loss_of_availability', 'loss_of_accountability',
    'financial_damage', 'reputation_damage', 'non_compliance', 'privacy_violation'
  ];
  
  requiredFactors.forEach(factor => {
    const value = riskFactors[factor];
    
    if (value === undefined || value === null) {
      errors.push(`${factor} is required`);
    } else {
      const numValue = parseFloat(value);
      if (isNaN(numValue) || numValue < 0 || numValue > 9) {
        errors.push(`${factor} must be a number between 0 and 9`);
      }
    }
  });
  
  return {
    isValid: errors.length === 0,
    errors
  };
};
