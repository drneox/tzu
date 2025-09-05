/**
 * Utilities for OWASP Risk Rating calculations
 */

/**
 * Calculate inherent risk using OWASP Risk Rating methodology
 * @param {Object} risk - Risk factors object
 * @returns {number} - Calculated inherent risk (0-9 scale)
 */
export const calculateInherentRisk = (risk) => {
  if (!risk) return 0;
  
  // OWASP Risk Rating: (Likelihood + Impact) / 2
  const likelihoodFactors = [
    // Threat Agent Factors
    risk.skill_level || 0,
    risk.motive || 0,
    risk.opportunity || 0,
    risk.size || 0,
    // Vulnerability Factors
    risk.ease_of_discovery || 0,
    risk.ease_of_exploit || 0,
    risk.awareness || 0,
    risk.intrusion_detection || 0
  ];
  
  const impactFactors = [
    // Technical Impact
    risk.loss_of_confidentiality || 0,
    risk.loss_of_integrity || 0,
    risk.loss_of_availability || 0,
    risk.loss_of_accountability || 0,
    // Business Impact
    risk.financial_damage || 0,
    risk.reputation_damage || 0,
    risk.non_compliance || 0,
    risk.privacy_violation || 0
  ];
  
  const likelihood = likelihoodFactors.reduce((acc, val) => acc + val, 0) / likelihoodFactors.length;
  const impact = impactFactors.reduce((acc, val) => acc + val, 0) / impactFactors.length;
  
  const overallRisk = (likelihood + impact) / 2;
  return parseFloat(overallRisk.toFixed(1)); // Changed to 1 decimal as requested
};

/**
 * Get risk level label based on OWASP scale
 * @param {number} riskValue - Risk value (0-9)
 * @param {Object} t - Localization object
 * @returns {string} - Risk level label
 */
export const getRiskLabel = (riskValue, t) => {
  const value = parseFloat(riskValue);
  if (value < 3) return t?.ui?.risk_low || "LOW";
  if (value < 6) return t?.ui?.risk_medium || "MEDIUM"; 
  return t?.ui?.risk_high || "HIGH";
};

/**
 * Get risk color scheme for UI components
 * @param {number} riskValue - Risk value (0-9)
 * @returns {string} - Chakra UI color scheme
 */
export const getRiskColorScheme = (riskValue) => {
  const value = parseFloat(riskValue);
  if (value >= 6) return 'red';
  if (value >= 3) return 'yellow';
  return 'green';
};

/**
 * Get risk color CSS value
 * @param {number} riskValue - Risk value (0-9)
 * @returns {string} - CSS color value
 */
export const getRiskColorCSS = (riskValue) => {
  const numericRisk = typeof riskValue === 'string' ? parseFloat(riskValue) : riskValue;
  if (numericRisk >= 6) return '#e53e3e'; // red.500
  if (numericRisk >= 3) return '#dd6b20'; // orange.500
  return '#38a169'; // green.500
};

/**
 * Validate OWASP risk factors
 * @param {Object} riskFactors - Risk factors object
 * @returns {Object} - Validation result with isValid flag and errors array
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
    if (value !== undefined && value !== null) {
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
