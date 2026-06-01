import React, { useState, useEffect, useRef } from 'react';
import {
  VStack, HStack, Text, Input, Box, Tag, TagLabel, TagCloseButton,
  Spinner, List, ListItem, Button, Alert, AlertIcon
} from "@chakra-ui/react";
import { fetchControlTagSuggestions, searchControlTags } from '../services';
import ControlTagTooltip from './ControlTagTooltip';
import { useControlTagsCatalog } from '../context/ControlTagsCatalogContext';

/**
 * Componente de Control Tags CON AUTOCOMPLETACIÓN REAL
 * Conectado al backend para sugerencias dinámicas
 */
const ControlTagsWithAutocomplete = ({ threatId, strideCategory, initialTags = [], onTagsChange }) => {
  // Catálogo cacheado (una sola petición por sesión)
  const { getTagDetails, isLoaded: catalogLoaded } = useControlTagsCatalog();

  // Estado principal
  const [tags, setTags] = useState(initialTags);
  const [inputValue, setInputValue] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [detailedSuggestions, setDetailedSuggestions] = useState([]); // Nuevo estado para sugerencias detalladas
  const [tagDetailsMap, setTagDetailsMap] = useState({}); // Mapa de detalles de tags
  const [isLoading, setIsLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [error, setError] = useState(null);

  // Referencias
  const inputRef = useRef(null);
  const suggestionsRef = useRef(null);

  // Cargar sugerencias iniciales basadas en STRIDE
  useEffect(() => {
    if (strideCategory) {
      loadInitialSuggestions();
    }
  }, [strideCategory]);

  // Cargar detalles para tags iniciales — esperar a que el catálogo esté listo
  useEffect(() => {
    if (catalogLoaded && initialTags && initialTags.length > 0) {
      loadTagDetailsForExistingTags(initialTags);
    }
  }, [catalogLoaded, initialTags]);

  // Notificar cambios al padre
  useEffect(() => {
    if (onTagsChange) {
      onTagsChange(threatId, tags);
    }
  }, [tags, threatId, onTagsChange]);

  // Función para obtener el color del tag basado en el estándar (misma lógica que el tooltip)
  const getTagColor = (tag) => {
    const tagDetails = tagDetailsMap[tag] || getTagDetails(tag);
    // Primary: standard from API details; Fallback: extract from "(STANDARD)" suffix
    const standard = tagDetails?.standard || tag.match(/\(([^)]+)\)$/)?.[1];
    
    switch (standard?.toUpperCase()) {
      case 'ASVS': return 'blue';
      case 'MASVS': return 'green';
      case 'NIST': return 'purple';
      case 'ISO27001': return 'orange';
      case 'SBS': return 'teal';
      default: return 'gray';
    }
  };

  /**
   * Carga detalles para tags existentes usando el catálogo cacheado (sin requests HTTP).
   */
  const loadTagDetailsForExistingTags = (existingTags) => {
    const detailsMap = {};
    for (const tag of existingTags) {
      const details = getTagDetails(tag);
      if (details) {
        detailsMap[tag] = details;
      } else {
        // Fallback: construir detalles mínimos desde el sufijo "(STANDARD)"
        const standardFromSuffix = tag.match(/\(([^)]+)\)$/)?.[1] || null;
        const baseTag = tag.replace(/\s*\([^)]+\)$/, '').trim();
        if (standardFromSuffix) {
          detailsMap[tag] = {
            standard: standardFromSuffix,
            category: null,
            title: baseTag,
            description: null,
          };
        }
      }
    }
    setTagDetailsMap(prev => ({ ...prev, ...detailsMap }));
  };

  /**
   * Carga sugerencias iniciales para la categoría STRIDE
   */
  const loadInitialSuggestions = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      console.log(`=== Loading suggestions for STRIDE: ${strideCategory} ===`);
      const data = await fetchControlTagSuggestions(strideCategory);
      console.log('Suggestions API response:', data);
      console.log('suggested_tags:', data.suggested_tags);
      
      setSuggestions(data.suggested_tags || []);
      setDetailedSuggestions(data.detailed_suggestions || []);
      
      // Crear mapa de detalles para los tags
      const detailsMap = {};
      if (data.detailed_suggestions) {
        data.detailed_suggestions.forEach(item => {
          // Para sugerencias STRIDE, usar formatted_tag como clave
          const keyTag = item.formatted_tag || item.tag;
          console.log(`Mapping suggestion: ${item.tag} -> ${keyTag}`, item);
          detailsMap[keyTag] = {
            standard: item.standard,
            category: item.category,
            title: item.title,
            description: item.description
          };
        });
      }
      console.log('Generated detailsMap for suggestions:', detailsMap);
      setTagDetailsMap(prev => ({ ...prev, ...detailsMap }));
      
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Busca tags mientras escribe el usuario
   */
  const searchTags = async (query) => {
    if (!query || query.length < 2) {
      // Si el query es muy corto, mostrar sugerencias de STRIDE
      await loadInitialSuggestions();
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      
      const data = await searchControlTags(query);
      setSuggestions(data.results || []);
      
      // Procesar detailed_results de la búsqueda
      // Indexar por ID bare Y por tag formateado para evitar mismatches
      const detailsMap = {};
      if (data.detailed_results) {
        data.detailed_results.forEach(item => {
          const entry = {
            standard: item.standard,
            category: item.category,
            title: item.title,
            description: item.description
          };
          detailsMap[item.tag] = entry;  // bare: "AUTH-2"
          if (item.standard) {
            detailsMap[`${item.tag} (${item.standard})`] = entry;  // formateado: "AUTH-2 (MASVS)"
          }
        });
      }
      setTagDetailsMap(prev => ({ ...prev, ...detailsMap }));
      
    } catch (err) {
      setError(err.message);
      setSuggestions([]);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Maneja cambios en el input
   */
  const handleInputChange = (e) => {
    const value = e.target.value;
    setInputValue(value);
    setShowSuggestions(true);
    
    // Debounce para no hacer demasiadas peticiones
    clearTimeout(window.searchTimeout);
    window.searchTimeout = setTimeout(() => {
      searchTags(value);
    }, 300);
  };

  /**
   * Agrega un tag
   */
  const addTag = async (tag) => {
    if (!tag || tags.includes(tag)) {
      return;
    }

    try {
      const newTags = [...tags, tag];
      setTags(newTags);
      setInputValue('');
      setShowSuggestions(false);
      setError(null); // Limpiar errores anteriores
      
    } catch (err) {
      setError(`Error al agregar tag: ${tag}`);
    }
  };

  /**
   * Elimina un tag
   */
  const removeTag = (tagToRemove) => {
    const newTags = tags.filter(tag => tag !== tagToRemove);
    setTags(newTags);
  };

  /**
   * Maneja teclas especiales
   */
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && inputValue.trim()) {
      e.preventDefault();
      addTag(inputValue.trim());
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
    }
  };

  /**
   * Oculta sugerencias al hacer clic fuera
   */
  const handleClickOutside = (e) => {
    if (
      inputRef.current && !inputRef.current.contains(e.target) &&
      suggestionsRef.current && !suggestionsRef.current.contains(e.target)
    ) {
      setShowSuggestions(false);
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <VStack align="start" spacing={3} w="100%" position="relative">
      <Text fontSize="sm" fontWeight="bold">
        Tags:
      </Text>

      {/* Error */}
      {error && (
        <Alert status="error" size="sm">
          <AlertIcon />
          {error}
        </Alert>
      )}

      {/* Tags existentes */}
      {tags.length > 0 && (
        <HStack wrap="wrap" spacing={1}>
          {tags.map((tag, index) => {
            return (
              <ControlTagTooltip
                key={index}
                tagDetails={tagDetailsMap[tag] || getTagDetails(tag)}
              >
                <Tag size="sm" colorScheme={getTagColor(tag)} variant="solid" cursor="help">
                  <TagLabel>{tag}</TagLabel>
                  <TagCloseButton onClick={() => removeTag(tag)} />
                </Tag>
              </ControlTagTooltip>
            );
          })}
        </HStack>
      )}

      {/* Input con autocompletación */}
      <Box position="relative" w="100%">
        <HStack>
          <Input
            ref={inputRef}
            placeholder="Escribe para buscar tags (ej: ASVS, MASVS, ISO27001)..."
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            onFocus={() => setShowSuggestions(true)}
            size="sm"
          />
          {isLoading && <Spinner size="sm" />}
        </HStack>

        {/* Lista de sugerencias */}
        {showSuggestions && suggestions.length > 0 && (
          <Box
            ref={suggestionsRef}
            position="absolute"
            top="100%"
            left={0}
            right={0}
            zIndex={1000}
            bg="white"
            border="1px solid"
            borderColor="gray.200"
            borderRadius="md"
            boxShadow="lg"
            maxH="200px"
            overflowY="auto"
            mt={1}
          >
            <List spacing={0}>
              {suggestions.map((suggestion, index) => (
                <ControlTagTooltip
                  key={index}
                  tagDetails={tagDetailsMap[suggestion] || getTagDetails(suggestion)}
                >
                  <ListItem
                    p={2}
                    cursor="pointer"
                    _hover={{ bg: "blue.50" }}
                    onClick={() => addTag(suggestion)}
                    fontSize="sm"
                    borderBottom="1px solid"
                    borderColor="gray.100"
                  >
                    {suggestion}
                  </ListItem>
                </ControlTagTooltip>
              ))}
            </List>
          </Box>
        )}
      </Box>

    </VStack>
  );
};

export default ControlTagsWithAutocomplete;
