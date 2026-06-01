/**
 * ControlTagsCatalogContext
 * Carga el catálogo completo de control tags UNA sola vez y lo cachea en memoria.
 * Elimina el patrón de N-requests por tag que saturaba nginx.
 */
import React, { createContext, useState, useEffect, useContext, useRef } from 'react';
import { searchControlTags } from '../services';
import { useAuth } from './AuthContext';

export const ControlTagsCatalogContext = createContext(null);

export const ControlTagsCatalogProvider = ({ children }) => {
  // Map<tagId, detailObject> — clave sin paréntesis, ej: "V4.3.1"
  const [catalog, setCatalog] = useState(new Map());
  const [isLoaded, setIsLoaded] = useState(false);
  const loadedRef = useRef(false);

  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isAuthenticated || loadedRef.current) return;

    const loadCatalog = async () => {
      try {
        // Traer todos los controles en una sola petición (limit alto para cubrir el catálogo completo)
        const data = await searchControlTags('', 500);
        const map = new Map();

        if (data.detailed_results) {
          data.detailed_results.forEach(item => {
            if (item.tag) {
              // Normalizar clave: quitar " (STANDARD)" si viniera formateado
              const key = item.tag.replace(/\s*\([^)]+\)$/, '').trim();
              map.set(key, {
                standard: item.standard || '',
                category: item.category || '',
                title: item.title || '',
                description: item.description || null,
              });
              // También indexar con el tag formateado por si acaso
              if (item.formatted_tag) {
                map.set(item.formatted_tag, map.get(key));
              }
            }
          });
        }

        setCatalog(map);
        setIsLoaded(true);
        loadedRef.current = true;
      } catch (err) {
        console.warn('ControlTagsCatalog: no se pudo cargar el catálogo', err);
        // No bloqueamos la app si falla; los componentes tienen su fallback
        setIsLoaded(true);
      }
    };

    loadCatalog();
  }, [isAuthenticated]);

  /**
   * Devuelve los detalles de un tag dado su ID o su forma formateada "V4.3.1 (ASVS)".
   * Retorna null si no está en el catálogo.
   */
  const getTagDetails = (tagInput) => {
    if (!tagInput) return null;
    // Intentar lookup directo
    if (catalog.has(tagInput)) return catalog.get(tagInput);
    // Normalizar quitando sufijo " (STANDARD)"
    const normalized = tagInput.replace(/\s*\([^)]+\)$/, '').trim();
    return catalog.get(normalized) || null;
  };

  return (
    <ControlTagsCatalogContext.Provider value={{ catalog, isLoaded, getTagDetails }}>
      {children}
    </ControlTagsCatalogContext.Provider>
  );
};

export const useControlTagsCatalog = () => useContext(ControlTagsCatalogContext);
