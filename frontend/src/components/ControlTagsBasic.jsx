import React from 'react';
import { VStack, HStack, Text, Input, Box, Tag, TagLabel, TagCloseButton } from "@chakra-ui/react";

// Componente BÁSICO para Control Tags - SIN AUTOCOMPLETAR PRIMERO
const ControlTagsBasic = ({ threatId, strideCategory, initialTags = [], onTagsChange }) => {
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
        <Text fontSize="xs" color="gray.600" mb={1}>Sugerencias de prueba (haz click):</Text>
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

export default ControlTagsBasic;
