import { useState, useCallback, useMemo } from 'react';
import { categorizeControlTags } from '../services/index';

/**
 * Hook personalizado para manejar la categorización de control tags
 * Mantiene un caché para evitar llamadas innecesarias al backend
 */
export const useTagCategorization = () => {
  const [cache, setCache] = useState({});
  const [loading, setLoading] = useState(false);

  /**
   * Categoriza una lista de tags, usando caché cuando sea posible
   */
  const categorizeTags = useCallback(async (tags) => {
    if (!tags || tags.length === 0) return {};

    // Crear clave de caché basada en los tags
    const cacheKey = JSON.stringify(tags.sort());
    
    // Si ya está en caché, devolverlo inmediatamente
    if (cache[cacheKey]) {
      return cache[cacheKey];
    }

    try {
      setLoading(true);
      const result = await categorizeControlTags(tags);
      
      // Usar la propiedad 'categorized' del resultado del backend
      const categorized = result.categorized || {};
      
      // Guardar en caché
      setCache(prev => ({
        ...prev,
        [cacheKey]: categorized
      }));
      
      return categorized;
    } catch (error) {
      console.error('Error categorizing tags:', error);
      
      // Fallback: categorización simple basada en prefijos
      const fallbackCategorized = {
        "ASVS": [],
        "MASVS": [],
        "SBS": [],
        "ISO27001": [],
        "NIST": [],
        "OTHER": []
      };
      
      tags.forEach(tag => {
        // Solo procesar tags que tengan el formato "control (standard)"
        const standardMatch = tag.match(/\(([^)]+)\)$/);
        
        if (standardMatch) {
          const standard = standardMatch[1].toUpperCase();
          
          // Categorizar basándose en el estándar dentro del paréntesis
          if (standard === 'ASVS') {
            fallbackCategorized["ASVS"].push(tag);
          } else if (standard === 'MASVS') {
            fallbackCategorized["MASVS"].push(tag);
          } else if (standard === 'ISO27001') {
            fallbackCategorized["ISO27001"].push(tag);
          } else if (standard === 'NIST') {
            fallbackCategorized["NIST"].push(tag);
          } else if (standard === 'SBS') {
            fallbackCategorized["SBS"].push(tag);
          } else {
            fallbackCategorized["OTHER"].push(tag);
          }
        } else {
          // Tags sin formato (standard) van a OTHER
          fallbackCategorized["OTHER"].push(tag);
        }
      });
      
      // Guardar fallback en caché
      setCache(prev => ({
        ...prev,
        [cacheKey]: fallbackCategorized
      }));
      
      return fallbackCategorized;
    } finally {
      setLoading(false);
    }
  }, [cache]);

  /**
   * Verifica si un tag pertenece a alguno de los estándares especificados
   */
  const tagBelongsToStandards = useCallback(async (tag, selectedStandards) => {
    if (!tag || !selectedStandards || selectedStandards.length === 0) {
      return false;
    }

    try {
      const categorized = await categorizeTags([tag]);
      
      // Verificar si el tag está en alguno de los estándares seleccionados
      return selectedStandards.some(standard => {
        const standardTags = categorized[standard] || [];
        return standardTags.includes(tag);
      });
    } catch (error) {
      console.error('Error checking tag belongs to standards:', error);
      return false;
    }
  }, [categorizeTags]);

  /**
   * Verificar si una amenaza coincide con los filtros de estándares
   */
  const threatMatchesStandardsFilter = useCallback(async (threat, selectedStandards) => {
    if (!selectedStandards || selectedStandards.length === 0) {
      return true;
    }

    if (!threat.remediation?.control_tags) {
      return false;
    }

    const controlTags = Array.isArray(threat.remediation.control_tags) 
      ? threat.remediation.control_tags 
      : [];

    if (controlTags.length === 0) {
      return false;
    }

    try {
      const categorized = await categorizeTags(controlTags);
      
      // Verificar si algún tag está en los estándares seleccionados
      return selectedStandards.some(standard => {
        const standardTags = categorized[standard] || [];
        return standardTags.length > 0;
      });
    } catch (error) {
      console.error('Error filtering threat by standards:', error);
      return false;
    }
  }, [categorizeTags]);

  /**
   * Filtra una lista de amenazas basándose en los estándares seleccionados
   */
  const filterThreatsByStandards = useCallback(async (threats, selectedStandards) => {
    if (!selectedStandards || selectedStandards.length === 0) {
      return threats;
    }

    if (!threats || threats.length === 0) {
      return [];
    }

    // Obtener todos los tags únicos de todas las amenazas
    const allTags = new Set();
    threats.forEach(threat => {
      if (threat.remediation?.control_tags) {
        const controlTags = Array.isArray(threat.remediation.control_tags) 
          ? threat.remediation.control_tags 
          : [];
        controlTags.forEach(tag => allTags.add(tag));
      }
    });

    // Categorizar todos los tags de una vez
    const categorized = await categorizeTags(Array.from(allTags));

    // Filtrar las amenazas
    return threats.filter(threat => {
      if (!threat.remediation?.control_tags) {
        return false;
      }

      const controlTags = Array.isArray(threat.remediation.control_tags) 
        ? threat.remediation.control_tags 
        : [];

      if (controlTags.length === 0) {
        return false;
      }

      // Verificar si algún tag está en los estándares seleccionados
      return selectedStandards.some(standard => {
        const standardTags = categorized[standard] || [];
        return controlTags.some(tag => standardTags.includes(tag));
      });
    });
  }, [categorizeTags]);

  /**
   * Contar amenazas que tienen controles de un estándar específico
   */
  const countThreatsWithStandard = useCallback(async (threats, standardName) => {
    if (!threats || threats.length === 0) return 0;

    try {
      const filtered = await filterThreatsByStandards(threats, [standardName]);
      return filtered.length;
    } catch (error) {
      console.error('Error counting threats with standard:', error);
      return 0;
    }
  }, [filterThreatsByStandards]);

  /**
   * Limpiar caché (útil para tests o cuando hay cambios en la configuración)
   */
  const clearCache = useCallback(() => {
    setCache({});
  }, []);

  return {
    categorizeTags,
    tagBelongsToStandards,
    threatMatchesStandardsFilter,
    filterThreatsByStandards,
    countThreatsWithStandard,
    clearCache,
    loading,
    cacheSize: Object.keys(cache).length
  };
};

export default useTagCategorization;
