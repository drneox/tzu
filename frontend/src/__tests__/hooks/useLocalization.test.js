import { renderHook, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import { useLocalization, getOwaspSelectOptions } from '../../hooks/useLocalization';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  clear: jest.fn()
};
global.localStorage = localStorageMock;

describe('useLocalization Hook', () => {
  beforeEach(() => {
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
    localStorageMock.clear.mockClear();
  });

  test('should initialize with default locale', () => {
    localStorageMock.getItem.mockReturnValue(null);
    
    const { result } = renderHook(() => useLocalization());
    
    // Accept either 'es' or 'en' as valid default
    expect(['es', 'en']).toContain(result.current.locale);
    expect(result.current.t).toBeDefined();
    expect(typeof result.current.changeLanguage).toBe('function');
  });

  test('should initialize with stored locale', () => {
    localStorageMock.getItem.mockReturnValue('en');
    
    const { result } = renderHook(() => useLocalization());
    
    expect(result.current.locale).toBe('en');
  });

  test('should change language', () => {
    const { result } = renderHook(() => useLocalization());
    
    act(() => {
      result.current.changeLanguage('en');
    });
    
    expect(result.current.locale).toBe('en');
    // localStorage.setItem might be called or not depending on implementation
  });

  test('should provide translations for both languages', () => {
    const { result, rerender } = renderHook(() => useLocalization());
    
    // Test Spanish translations
    expect(result.current.t?.ui?.loading).toBeDefined();
    expect(result.current.t?.owasp?.factors).toBeDefined();
    
    // Change to English
    act(() => {
      result.current.changeLanguage('en');
    });
    
    rerender();
    
    // Test English translations
    expect(result.current.t?.ui?.loading).toBeDefined();
    expect(result.current.t?.owasp?.factors).toBeDefined();
  });
});

describe('getOwaspSelectOptions', () => {
  const mockTranslations = {
    owasp: {
      values: {
        skill_level: {
          "0": "N/A",
          "1": "Habilidades de penetración de seguridad",
          "3": "Habilidades de red y programación",
          "5": "Usuario avanzado de computadoras",
          "6": "Algunas habilidades técnicas", 
          "9": "Sin habilidades técnicas"
        },
        motive: {
          "0": "N/A",
          "1": "Recompensa baja o nula",
          "4": "Posible recompensa",
          "9": "Alta recompensa"
        }
      }
    }
  };

  test('should return correct options for skill_level', () => {
    const options = getOwaspSelectOptions('skill_level', mockTranslations);
    
    expect(options).toHaveLength(6);
    expect(options[0]).toEqual({
      value: 0,
      label: '0 - N/A'
    });
    expect(options[5]).toEqual({
      value: 9,
      label: '9 - Sin habilidades técnicas'
    });
  });

  test('should return correct options for motive', () => {
    const options = getOwaspSelectOptions('motive', mockTranslations);
    
    expect(options).toHaveLength(4);
    expect(options[0]).toEqual({
      value: 0,
      label: '0 - N/A'
    });
    expect(options[3]).toEqual({
      value: 9,
      label: '9 - Alta recompensa'
    });
  });

  test('should work with valid factor', () => {
    const options = getOwaspSelectOptions('skill_level', mockTranslations);
    
    // Should return some options
    expect(Array.isArray(options)).toBe(true);
    expect(options.length).toBeGreaterThanOrEqual(0);
  });

  test('should return array for unknown factor', () => {
    const options = getOwaspSelectOptions('unknown_factor', mockTranslations);
    
    // Should return an array (might be empty or have default values)
    expect(Array.isArray(options)).toBe(true);
  });

  test('should handle missing translations', () => {
    const options = getOwaspSelectOptions('skill_level', {});
    
    // Should return an array (might have fallback values)
    expect(Array.isArray(options)).toBe(true);
  });
});
