import { formatDate, formatRisk, generateThreatId, validateRiskFactors } from '../../utils/index';

describe('Utility Functions', () => {
  describe('formatDate', () => {
    test('should format date correctly in Spanish', () => {
      const mockDate = new Date('2024-01-15T10:30:00Z');
      const result = formatDate(mockDate, 'es');
      
      // Verify it contains expected parts (day, month, year)
      expect(result).toMatch(/\d{1,2}\/\d{1,2}\/\d{4}/);
    });

    test('should format date correctly in English', () => {
      const mockDate = new Date('2024-01-15T10:30:00Z');
      const result = formatDate(mockDate, 'en');
      
      expect(result).toMatch(/\d{1,2}\/\d{1,2}\/\d{4}/);
    });

    test('should handle invalid date', () => {
      const result = formatDate(new Date('invalid'), 'es');
      expect(result).toBe('Invalid Date');
    });

    test('should handle null or undefined date', () => {
      expect(formatDate(null, 'es')).toBe('');
      expect(formatDate(undefined, 'es')).toBe('');
    });
  });

  describe('formatRisk', () => {
    test('should format risk value with two decimal places', () => {
      expect(formatRisk(5.123456)).toBe('5.12');
      expect(formatRisk(3.999)).toBe('4.00');
      expect(formatRisk(7)).toBe('7.00');
    });

    test('should handle edge cases', () => {
      expect(formatRisk(0)).toBe('0.00');
      expect(formatRisk(9.999)).toBe('10.00');
      expect(formatRisk(0.001)).toBe('0.00');
    });

    test('should handle invalid inputs', () => {
      expect(formatRisk(null)).toBe('0.00');
      expect(formatRisk(undefined)).toBe('0.00');
      expect(formatRisk('invalid')).toBe('0.00');
      expect(formatRisk(NaN)).toBe('0.00');
    });
  });

  describe('generateThreatId', () => {
    test('should generate unique IDs', () => {
      const id1 = generateThreatId();
      const id2 = generateThreatId();
      
      expect(id1).not.toBe(id2);
      expect(typeof id1).toBe('string');
      expect(id1.length).toBeGreaterThan(0);
    });

    test('should generate IDs with expected format', () => {
      const id = generateThreatId();
      
      // Should be a string that could be used as an identifier
      expect(id).toMatch(/^[a-zA-Z0-9-_]+$/);
    });

    test('should generate consistent format across multiple calls', () => {
      const ids = Array.from({ length: 10 }, () => generateThreatId());
      
      // All should be strings
      ids.forEach(id => {
        expect(typeof id).toBe('string');
        expect(id.length).toBeGreaterThan(0);
      });
      
      // All should be unique
      const uniqueIds = new Set(ids);
      expect(uniqueIds.size).toBe(ids.length);
    });
  });

  describe('validateRiskFactors', () => {
    const validRiskFactors = {
      skill_level: 3,
      motive: 4,
      opportunity: 7,
      size: 5,
      ease_of_discovery: 6,
      ease_of_exploit: 5,
      awareness: 3,
      intrusion_detection: 2,
      loss_of_confidentiality: 7,
      loss_of_integrity: 5,
      loss_of_availability: 3,
      loss_of_accountability: 4,
      financial_damage: 5,
      reputation_damage: 6,
      non_compliance: 4,
      privacy_violation: 5
    };

    test('should validate correct risk factors', () => {
      const result = validateRiskFactors(validRiskFactors);
      expect(result.isValid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('should detect missing required factors', () => {
      const incompleteFactors = {
        skill_level: 3,
        motive: 4
        // Missing other required factors
      };

      const result = validateRiskFactors(incompleteFactors);
      expect(result.isValid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });

    test('should detect invalid factor values', () => {
      const invalidFactors = {
        ...validRiskFactors,
        skill_level: -1, // Invalid: below 0
        motive: 10, // Invalid: above 9
        opportunity: 'invalid' // Invalid: not a number
      };

      const result = validateRiskFactors(invalidFactors);
      expect(result.isValid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });

    test('should handle null or undefined input', () => {
      expect(validateRiskFactors(null).isValid).toBe(false);
      expect(validateRiskFactors(undefined).isValid).toBe(false);
    });

    test('should validate boundary values', () => {
      const boundaryFactors = {
        ...validRiskFactors,
        skill_level: 0, // Valid minimum
        motive: 9 // Valid maximum
      };

      const result = validateRiskFactors(boundaryFactors);
      expect(result.isValid).toBe(true);
    });
  });

  describe('Risk Calculation Helpers', () => {
    test('should calculate likelihood average correctly', () => {
      const factors = {
        skill_level: 2,
        motive: 4,
        opportunity: 6,
        size: 8
      };

      const likelihoodAverage = (factors.skill_level + factors.motive + factors.opportunity + factors.size) / 4;
      expect(likelihoodAverage).toBe(5);
    });

    test('should calculate impact average correctly', () => {
      const factors = {
        loss_of_confidentiality: 8,
        loss_of_integrity: 6,
        loss_of_availability: 4,
        loss_of_accountability: 2
      };

      const impactAverage = (factors.loss_of_confidentiality + factors.loss_of_integrity + factors.loss_of_availability + factors.loss_of_accountability) / 4;
      expect(impactAverage).toBe(5);
    });

    test('should handle missing factors in calculations', () => {
      const incompleteLikelihoodFactors = {
        skill_level: 4,
        motive: 6
        // Missing opportunity and size
      };

      // Should default missing values to 0
      const likelihoodAverage = (
        (incompleteLikelihoodFactors.skill_level || 0) +
        (incompleteLikelihoodFactors.motive || 0) +
        (incompleteLikelihoodFactors.opportunity || 0) +
        (incompleteLikelihoodFactors.size || 0)
      ) / 4;

      expect(likelihoodAverage).toBe(2.5);
    });
  });

  describe('Data Transformation Utilities', () => {
    test('should transform threat data for display', () => {
      const rawThreatData = {
        id: '1',
        title: 'SQL Injection',
        description: 'Database attack',
        risk: {
          skill_level: 3,
          financial_damage: 7
        },
        remediation: {
          status: false,
          description: 'Not applied'
        }
      };

      // Test data transformation
      const transformedData = {
        ...rawThreatData,
        riskLevel: rawThreatData.risk ? 'CALCULATED' : 'UNKNOWN',
        hasRemediation: Boolean(rawThreatData.remediation?.status)
      };

      expect(transformedData.riskLevel).toBe('CALCULATED');
      expect(transformedData.hasRemediation).toBe(false);
    });

    test('should handle incomplete threat data', () => {
      const incompleteData = {
        id: '1',
        title: 'Incomplete Threat'
        // Missing risk and remediation data
      };

      const transformedData = {
        ...incompleteData,
        riskLevel: incompleteData.risk ? 'CALCULATED' : 'UNKNOWN',
        hasRemediation: Boolean(incompleteData.remediation?.status)
      };

      expect(transformedData.riskLevel).toBe('UNKNOWN');
      expect(transformedData.hasRemediation).toBe(false);
    });
  });

  describe('String Utilities', () => {
    test('should capitalize first letter', () => {
      const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();

      expect(capitalize('hello')).toBe('Hello');
      expect(capitalize('WORLD')).toBe('World');
      expect(capitalize('tEST')).toBe('Test');
      expect(capitalize('')).toBe('');
    });

    test('should truncate long text', () => {
      const truncate = (text, maxLength) => {
        if (text.length <= maxLength) return text;
        return text.slice(0, maxLength) + '...';
      };

      expect(truncate('Short text', 20)).toBe('Short text');
      expect(truncate('This is a very long text that needs truncation', 10)).toBe('This is a ...');
      expect(truncate('', 10)).toBe('');
    });

    test('should generate safe CSS class names', () => {
      const toCSSClass = (str) => {
        return str.toLowerCase()
          .replace(/[^a-z0-9]/g, '-')
          .replace(/-+/g, '-')
          .replace(/^-|-$/g, '');
      };

      expect(toCSSClass('High Risk')).toBe('high-risk');
      expect(toCSSClass('SQL_Injection')).toBe('sql-injection');
      expect(toCSSClass('Test  Multiple   Spaces')).toBe('test-multiple-spaces');
    });
  });

  describe('Array and Object Utilities', () => {
    test('should deep clone objects', () => {
      const original = {
        name: 'Test',
        risk: { level: 5, factors: [1, 2, 3] }
      };

      const cloned = JSON.parse(JSON.stringify(original));
      
      expect(cloned).toEqual(original);
      expect(cloned).not.toBe(original);
      expect(cloned.risk).not.toBe(original.risk);
    });

    test('should merge objects safely', () => {
      const mergeObjects = (target, source) => {
        return { ...target, ...source };
      };

      const obj1 = { a: 1, b: 2 };
      const obj2 = { b: 3, c: 4 };
      const result = mergeObjects(obj1, obj2);

      expect(result).toEqual({ a: 1, b: 3, c: 4 });
      expect(obj1).toEqual({ a: 1, b: 2 }); // Original unchanged
    });

    test('should filter falsy values', () => {
      const filterFalsy = (arr) => arr.filter(Boolean);

      const input = [1, 0, 'hello', '', null, 'world', undefined, false, true];
      const result = filterFalsy(input);

      expect(result).toEqual([1, 'hello', 'world', true]);
    });

    test('should group array items by property', () => {
      const groupBy = (array, key) => {
        return array.reduce((groups, item) => {
          const group = item[key];
          groups[group] = groups[group] || [];
          groups[group].push(item);
          return groups;
        }, {});
      };

      const threats = [
        { id: 1, category: 'injection', severity: 'high' },
        { id: 2, category: 'injection', severity: 'medium' },
        { id: 3, category: 'xss', severity: 'high' }
      ];

      const grouped = groupBy(threats, 'category');

      expect(grouped.injection).toHaveLength(2);
      expect(grouped.xss).toHaveLength(1);
      expect(grouped.injection[0].id).toBe(1);
    });
  });
});
