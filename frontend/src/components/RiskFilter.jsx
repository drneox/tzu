import React from 'react';
import {
  Box,
  Text,
  HStack,
  Button,
  Badge,
  VStack
} from '@chakra-ui/react';

const RiskFilter = ({ 
  selectedInherentRisk, 
  selectedCurrentRisk, 
  onInherentRiskChange, 
  onCurrentRiskChange 
}) => {
  const riskLevels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
  
  const getRiskColor = (level) => {
    switch(level) {
      case 'LOW': return 'green';
      case 'MEDIUM': return 'yellow';
      case 'HIGH': return 'orange';
      case 'CRITICAL': return 'red';
      default: return 'gray';
    }
  };

  const getRiskText = (level) => {
    switch(level) {
      case 'LOW': return 'Bajo';
      case 'MEDIUM': return 'Medio';
      case 'HIGH': return 'Alto';
      case 'CRITICAL': return 'Crítico';
      default: return level;
    }
  };

  return (
    <Box p={4} border="1px" borderColor="gray.200" borderRadius="md">
      <VStack spacing={4} align="stretch">
        <Box>
          <Text fontWeight="bold" mb={2}>Riesgo Inherente</Text>
          <HStack spacing={2} wrap="wrap">
            <Button
              size="sm"
              variant={selectedInherentRisk === null ? "solid" : "outline"}
              colorScheme="blue"
              onClick={() => onInherentRiskChange(null)}
            >
              Todos
            </Button>
            {riskLevels.map((level) => (
              <Button
                key={level}
                size="sm"
                variant={selectedInherentRisk === level ? "solid" : "outline"}
                colorScheme={getRiskColor(level)}
                onClick={() => onInherentRiskChange(level)}
              >
                {getRiskText(level)}
              </Button>
            ))}
          </HStack>
        </Box>

        <Box>
          <Text fontWeight="bold" mb={2}>Riesgo Actual</Text>
          <HStack spacing={2} wrap="wrap">
            <Button
              size="sm"
              variant={selectedCurrentRisk === null ? "solid" : "outline"}
              colorScheme="blue"
              onClick={() => onCurrentRiskChange(null)}
            >
              Todos
            </Button>
            {riskLevels.map((level) => (
              <Button
                key={level}
                size="sm"
                variant={selectedCurrentRisk === level ? "solid" : "outline"}
                colorScheme={getRiskColor(level)}
                onClick={() => onCurrentRiskChange(level)}
              >
                {getRiskText(level)}
              </Button>
            ))}
          </HStack>
        </Box>

        {(selectedInherentRisk || selectedCurrentRisk) && (
          <Box>
            <Text fontSize="sm" color="gray.600">Filtros activos:</Text>
            <HStack spacing={2} mt={1}>
              {selectedInherentRisk && (
                <Badge colorScheme={getRiskColor(selectedInherentRisk)} size="sm">
                  Inherente: {getRiskText(selectedInherentRisk)}
                </Badge>
              )}
              {selectedCurrentRisk && (
                <Badge colorScheme={getRiskColor(selectedCurrentRisk)} size="sm">
                  Actual: {getRiskText(selectedCurrentRisk)}
                </Badge>
              )}
            </HStack>
          </Box>
        )}
      </VStack>
    </Box>
  );
};

export default RiskFilter;
