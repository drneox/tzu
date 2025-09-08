import Reacimport React from 'react';
import { VStack, HStack, Text, Input, Box, Tag, TagLabel, TagCloseButton } from "@chakra-ui/react";

// Componente BÁSICO para Control Tags - SIN AUTOCOMPLETAR PRIMERO
const ControlTagsSimple = ({ threatId, strideCategory, initialTags = [], onTagsChange }) => {
  const [tags, setTags] = React.useState(initialTags);
  const [inputValue, setInputValue] = React.useState('');

  console.log(`🔥 BÁSICO RENDER threatId=${threatId}, strideCategory=${strideCategory}`);

  // Solo notificar cambios al padre
  React.useEffect(() => {
    if (onTagsChange) {
      onTagsChange(threatId, tags);
    }
  }, [tags, threatId, onTagsChange]);

  const addTag = (tag) => {
    if (tag && !tags.includes(tag)) {
      const newTags = [...tags, tag];
      setTags(newTags);
      setInputValue('');
      console.log(`➕ TAG AGREGADO: ${tag}`);
    }
  };

  const removeTag = (tagToRemove) => {
    const newTags = tags.filter(tag => tag !== tagToRemove);
    setTags(newTags);
    console.log(`➖ TAG ELIMINADO: ${tagToRemove}`);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && inputValue.trim()) {
      e.preventDefault();
      addTag(inputValue.trim());
    }
  };

  // Tags predefinidos para testing
  const testTags = ['ASVS-V2.1.1', 'ASVS-V2.2.1', 'MASVS-MSTG-AUTH-1', 'ISO27001-A.9.1.1'];

  return (
    <VStack align="start" spacing={2} w="100%">
      <Text fontSize="sm" fontWeight="bold">Tags:</Text>
      
      {/* Tags existentes */}
      {tags.length > 0 && (
        <HStack wrap="wrap" spacing={1}>
          {tags.map((tag, index) => (
            <Tag key={index} size="sm" colorScheme="blue">
              <TagLabel>{tag}</TagLabel>
              <TagCloseButton onClick={() => removeTag(tag)} />
            </Tag>
          ))}
        </HStack>
      )}

      {/* Input manual */}
      <Input
        value={inputValue}
        onChange={(e) => {
          console.log(`⌨️ ESCRIBIENDO: "${e.target.value}"`);
          setInputValue(e.target.value);
        }}
        onKeyDown={handleKeyDown}
        placeholder="Escribe un tag y presiona Enter (ej: ASVS-V2.1.1)"
        size="sm"
        bg="white"
      />

      {/* Sugerencias de prueba */}
      <Box>
        <Text fontSize="xs" color="gray.600" mb={1}>Sugerencias de prueba:</Text>
        <HStack wrap="wrap" spacing={1}>
          {testTags.map((tag) => (
            <Tag 
              key={tag} 
              size="xs" 
              colorScheme="green" 
              cursor="pointer"
              onClick={() => addTag(tag)}
            >
              <TagLabel>{tag}</TagLabel>
            </Tag>
          ))}
        </HStack>
      </Box>
      
      <Text fontSize="xs" color="gray.500">
        Debug: STRIDE={strideCategory} | Tags={tags.length} | Input="{inputValue}"
      </Text>
    </VStack>
  );
};

export default ControlTagsSimple; from 'react';
import { VStack, HStack, Text, Input, Box, Tag, TagLabel, TagCloseButton } from "@chakra-ui/react";
import { fetchControlTagSuggestions } from "../services/index";

// Componente SÚPER SIMPLE para Control Tags
const ControlTagsSimple = ({ threatId, strideCategory, initialTags = [], onTagsChange }) => {
  const [tags, setTags] = React.useState(initialTags);
  const [inputValue, setInputValue] = React.useState('');
  const [suggestions, setSuggestions] = React.useState([]);
  const [showSuggestions, setShowSuggestions] = React.useState(false);

  console.log(`� RENDER threatId=${threatId}, strideCategory=${strideCategory}, suggestions=${suggestions.length}`);

  // Cargar sugerencias inmediatamente cuando se monta el componente
  React.useEffect(() => {
    if (strideCategory) {
      console.log(`🌐 CARGANDO SUGERENCIAS para ${strideCategory}`);
      fetchControlTagSuggestions(strideCategory)
        .then(data => {
          console.log(`✅ SUGERENCIAS CARGADAS:`, data.suggested_tags);
          setSuggestions(data.suggested_tags || []);
        })
        .catch(err => {
          console.error(`❌ ERROR:`, err);
        });
    }
  }, [strideCategory]);

  // Notificar cambios al padre
  React.useEffect(() => {
    if (onTagsChange) {
      onTagsChange(threatId, tags);
    }
  }, [tags, threatId, onTagsChange]);

  const handleInputChange = (e) => {
    const value = e.target.value;
    console.log(`⌨️ ESCRIBIENDO: "${value}"`);
    setInputValue(value);
    setShowSuggestions(true);
  };

  const addTag = (tag) => {
    if (tag && !tags.includes(tag)) {
      const newTags = [...tags, tag];
      setTags(newTags);
      setInputValue('');
      setShowSuggestions(false);
      console.log(`➕ TAG AGREGADO: ${tag}`);
    }
  };

  const removeTag = (tagToRemove) => {
    const newTags = tags.filter(tag => tag !== tagToRemove);
    setTags(newTags);
    console.log(`➖ TAG ELIMINADO: ${tagToRemove}`);
  };

  // Filtrar sugerencias en tiempo real
  const filteredSuggestions = suggestions
    .filter(tag => tag.toLowerCase().includes(inputValue.toLowerCase()) && !tags.includes(tag))
    .slice(0, 5);

  console.log(`🔍 INPUT="${inputValue}" FILTRADAS=${filteredSuggestions.length} MOSTRAR=${showSuggestions}`);

  return (
    <VStack align="start" spacing={2} w="100%">
      <Text fontSize="sm" fontWeight="bold">Tags:</Text>
      
      {/* Tags existentes */}
      {tags.length > 0 && (
        <HStack wrap="wrap" spacing={1}>
          {tags.map((tag, index) => (
            <Tag key={index} size="sm" colorScheme="blue">
              <TagLabel>{tag}</TagLabel>
              <TagCloseButton onClick={() => removeTag(tag)} />
            </Tag>
          ))}
        </HStack>
      )}

      {/* Input */}
      <Box position="relative" w="100%">
        <Input
          value={inputValue}
          onChange={handleInputChange}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && inputValue.trim()) {
              e.preventDefault();
              addTag(inputValue.trim());
            }
          }}
          placeholder="Escribe para buscar tags (ej: ASVS)"
          size="sm"
          bg="white"
        />

        {/* Sugerencias */}
        {showSuggestions && filteredSuggestions.length > 0 && (
          <Box
            position="absolute"
            top="100%"
            left={0}
            right={0}
            bg="white"
            border="1px solid #ccc"
            borderRadius="md"
            maxH="150px"
            overflowY="auto"
            zIndex={1000}
            boxShadow="0 4px 6px rgba(0,0,0,0.1)"
          >
            {filteredSuggestions.map((tag, index) => (
              <Box
                key={index}
                p={2}
                cursor="pointer"
                _hover={{ bg: "blue.50" }}
                onClick={() => addTag(tag)}
                fontSize="sm"
                borderBottom={index < filteredSuggestions.length - 1 ? "1px solid #eee" : "none"}
              >
                {tag}
              </Box>
            ))}
          </Box>
        )}
      </Box>
      
      <Text fontSize="xs" color="gray.500">
        Debug: STRIDE={strideCategory} | Tags={tags.length} | Suggestions={suggestions.length} | Showing={showSuggestions ? 'YES' : 'NO'}
      </Text>
    </VStack>
  );
};

export default ControlTagsSimple;
