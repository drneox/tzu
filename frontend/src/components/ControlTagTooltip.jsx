import React from 'react';
import {
  Tooltip,
  Box,
  Text,
  Badge,
  VStack,
  HStack,
  Divider
} from "@chakra-ui/react";

/**
 * Componente de tooltip para mostrar detalles de control tags
 */
const ControlTagTooltip = ({ children, tagDetails, isOpen, ...tooltipProps }) => {
  if (!tagDetails) {
    return children;
  }

  const { standard, category, title, description } = tagDetails;

  // Colores por estándar
  const getStandardColor = (std) => {
    switch (std?.toUpperCase()) {
      case 'ASVS': return 'blue';
      case 'MASVS': return 'green';
      case 'NIST': return 'purple';
      case 'ISO27001': return 'orange';
      case 'SBS': return 'teal';
      default: return 'gray';
    }
  };

  const tooltipContent = (
    <Box maxW="300px" p={2}>
      <VStack align="start" spacing={2}>
        {/* Header con estándar y categoría */}
        <HStack justify="space-between" w="100%">
          <Badge 
            colorScheme={getStandardColor(standard)} 
            variant="solid" 
            fontSize="xs"
          >
            {standard}
          </Badge>
          {category && (
            <Text fontSize="xs" color="gray.300">
              {category}
            </Text>
          )}
        </HStack>

        <Divider />

        {/* Título */}
        {title && (
          <Text fontWeight="bold" fontSize="sm" color="white">
            {title}
          </Text>
        )}

        {/* Descripción */}
        {description && (
          <Text fontSize="xs" color="gray.200" lineHeight="1.4">
            {description}
          </Text>
        )}
      </VStack>
    </Box>
  );

  return (
    <Tooltip
      label={tooltipContent}
      placement="top"
      hasArrow
      bg="gray.800"
      color="white"
      borderRadius="md"
      fontSize="sm"
      isOpen={isOpen}
      {...tooltipProps}
    >
      {children}
    </Tooltip>
  );
};

export default ControlTagTooltip;
