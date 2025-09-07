import React, { useState, useEffect, useRef } from 'react';
import {
  VStack, HStack, Text, Input, Box, Tag, TagLabel, TagCloseButton,
  Spinner, List, ListItem, Button, Alert, AlertIcon
} from "@chakra-ui/react";
import { fetchControlTagSuggestions, searchControlTags } from '../services';
import ControlTagTooltip from './ControlTagTooltip';

/**
 * Componente de Control Tags CON AUTOCOMPLETACIÓN REAL
 * Conectado al backend para sugerencias dinámicas
 */
const ControlTagsWithAutocomplete = ({ threatId, strideCategory, initialTags = [], onTagsChange }) => {
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

  // Cargar detalles para tags iniciales
  useEffect(() => {
    if (initialTags && initialTags.length > 0) {
      loadTagDetailsForExistingTags(initialTags);
    }
  }, [initialTags]);

  // Notificar cambios al padre
  useEffect(() => {
    if (onTagsChange) {
      onTagsChange(threatId, tags);
    }
  }, [tags, threatId, onTagsChange]);

  // Función para obtener el color del tag basado en el estándar (misma lógica que el tooltip)
  const getTagColor = (tag) => {
    const tagDetails = tagDetailsMap[tag];
    const standard = tagDetails?.standard;
    
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
   * Carga detalles para tags que ya existen (initialTags)
   */
  const loadTagDetailsForExistingTags = async (existingTags) => {
    console.log('loadTagDetailsForExistingTags - existingTags:', existingTags);
    
    try {
      setIsLoading(true);
      
      // Cargar detalles para cada tag existente
      const detailsMap = {};
      
      for (const tag of existingTags) {
        try {
          console.log(`Buscando detalles para tag: ${tag}`);
          
          // Extraer el tag base si viene formateado con paréntesis
          const extractBaseTag = (tagStr) => {
            const match = tagStr.match(/^(.+?)\s*\([^)]+\)$/);
            return match ? match[1].trim() : tagStr;
          };
          
          const baseTag = extractBaseTag(tag);
          console.log(`Tag base extraído: ${baseTag}`);
          
          // Buscar usando el tag base para mayor flexibilidad
          const data = await searchControlTags(baseTag);
          console.log(`Respuesta para ${tag}:`, data);
          
          if (data.detailed_results && data.detailed_results.length > 0) {
            // Buscar el resultado que coincida con nuestro tag formateado
            let tagDetail = data.detailed_results.find(item => item.tag === tag);
            
            // Si no encuentra coincidencia exacta, buscar por tag base
            if (!tagDetail) {
              tagDetail = data.detailed_results.find(item => {
                const itemBaseTag = extractBaseTag(item.tag);
                return itemBaseTag === baseTag;
              });
            }
            
            if (tagDetail) {
              detailsMap[tag] = {
                standard: tagDetail.standard,
                category: tagDetail.category,
                title: tagDetail.title,
                description: tagDetail.description
              };
              console.log(`Detalles cargados para ${tag}:`, detailsMap[tag]);
            } else {
              console.warn(`No se encontró detalle específico para tag: ${tag}`);
            }
          } else {
            console.warn(`No hay detailed_results para tag: ${tag}`);
          }
        } catch (err) {
          console.warn(`Error cargando detalles para el tag: ${tag}`, err);
        }
      }
      
      console.log('detailsMap final:', detailsMap);
      setTagDetailsMap(prev => {
        const newMap = { ...prev, ...detailsMap };
        console.log('tagDetailsMap actualizado:', newMap);
        return newMap;
      });
      
    } catch (err) {
      console.error('Error cargando detalles de tags existentes:', err);
    } finally {
      setIsLoading(false);
    }
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
      const detailsMap = {};
      if (data.detailed_results) {
        data.detailed_results.forEach(item => {
          detailsMap[item.tag] = {
            standard: item.standard,
            category: item.category,
            title: item.title,
            description: item.description
          };
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
            // Debug: Log para verificar tagDetailsMap
            console.log(`Tag: ${tag}, Details:`, tagDetailsMap[tag]);
            
            return (
              <ControlTagTooltip
                key={index}
                tagDetails={tagDetailsMap[tag]}
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
                  tagDetails={tagDetailsMap[suggestion]}
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
