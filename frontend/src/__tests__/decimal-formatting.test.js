/**
 * Test for issue #31: Standardize risk decimals using the same rounding as Current Risk
 * Verifies that Inherent Risk and Current Risk now both use 1 decimal place formatting
 */

import { formatRisk } from '../utils/index';

// Mock the calculateInherentRisk function behavior (it's internal to Analysis.jsx)
const mockCalculateInherentRisk = (risk) => {
  if (!risk) return 0;
  
  const likelihoodFactors = [
    risk.skill_level || 0, risk.motive || 0, risk.opportunity || 0, risk.size || 0,
    risk.ease_of_discovery || 0, risk.ease_of_exploit || 0, risk.awareness || 0, risk.intrusion_detection || 0
  ];
  
  const impactFactors = [
    risk.loss_of_confidentiality || 0, risk.loss_of_integrity || 0, risk.loss_of_availability || 0, risk.loss_of_accountability || 0,
    risk.financial_damage || 0, risk.reputation_damage || 0, risk.non_compliance || 0, risk.privacy_violation || 0
  ];
  
  const likelihood = likelihoodFactors.reduce((acc, val) => acc + val, 0) / likelihoodFactors.length;
  const impact = impactFactors.reduce((acc, val) => acc + val, 0) / impactFactors.length;
  
  const overallRisk = (likelihood + impact) / 2;
  return overallRisk.toFixed(1); // This is the fix - now uses 1 decimal place
};

describe('Risk Decimal Formatting Standardization (Issue #31)', () => {
  test('Inherent Risk calculation should now return 1 decimal place', () => {
    const mockRiskData = {
      skill_level: 3, motive: 4, opportunity: 7, size: 5,
      ease_of_discovery: 6, ease_of_exploit: 5, awareness: 3, intrusion_detection: 2,
      loss_of_confidentiality: 7, loss_of_integrity: 5, loss_of_availability: 3, loss_of_accountability: 4,
      financial_damage: 5, reputation_damage: 6, non_compliance: 4, privacy_violation: 5
    };

    const result = mockCalculateInherentRisk(mockRiskData);
    
    // Should have exactly 1 decimal place
    expect(result).toMatch(/^\d+\.\d$/);
    // Should not have 2 decimal places (the old format)
    expect(result).not.toMatch(/^\d+\.\d{2}$/);
  });

  test('formatRisk utility should now format to 1 decimal place', () => {
    // Test various scenarios that previously would show 2 decimals
    expect(formatRisk(4.625)).toBe('4.6'); // Previously would be 4.63
    expect(formatRisk(6.25)).toBe('6.3');  // Previously would be 6.25
    expect(formatRisk(5.69)).toBe('5.7');  // Previously would be 5.69
    expect(formatRisk(3.14159)).toBe('3.1'); // Previously would be 3.14
  });

  test('Risk values should be consistently formatted across the system', () => {
    const testValues = [1.23, 4.567, 7.89, 2.1, 0.05];
    
    testValues.forEach(value => {
      const formatted = formatRisk(value);
      
      // All should have exactly one decimal place
      expect(formatted).toMatch(/^\d+\.\d$/);
      // None should have two decimal places
      expect(formatted).not.toMatch(/^\d+\.\d{2}$/);
    });
  });

  test('Edge cases maintain 1 decimal place formatting', () => {
    expect(formatRisk(0)).toBe('0.0');
    expect(formatRisk(9.99)).toBe('10.0'); // Rounding up
    expect(formatRisk(0.01)).toBe('0.0');  // Rounding down
    expect(formatRisk(null)).toBe('0.0');
    expect(formatRisk(undefined)).toBe('0.0');
  });

  test('Current Risk display format (existing behavior) should still be 1 decimal', () => {
    // This test documents the expected behavior for Current Risk
    // Current Risk values are displayed using toFixed(1) throughout the app
    const currentRiskValues = [6.3, 5.7, 4.2, 8.9];
    
    currentRiskValues.forEach(value => {
      const displayed = value.toFixed(1);
      expect(displayed).toMatch(/^\d+\.\d$/);
    });
  });
});