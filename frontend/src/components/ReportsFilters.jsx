/**
 * Componente ReportsFilters
 * Panel de filtros para la página de reportes
 */
import React from 'react';
import {
  Box,
  Button,
  HStack,
  VStack,
  Text,
  Badge
} from '@chakra-ui/react';
import { useLocalization } from '../hooks/useLocalization';

/**
 * Componente StandardsFilter
 * Filtro por estándares de seguridad
 */
const StandardsFilter = ({ 
  selectedStandards, 
  onStandardToggle,
  availableStandards
}) => {
  const { t } = useLocalization();
  
  const standardsData = [
    { value: 'ASVS', label: 'ASVS', color: 'blue' },
    { value: 'MASVS', label: 'MASVS', color: 'purple' },
    { value: 'ISO27001', label: 'ISO 27001', color: 'green' },
    { value: 'NIST', label: 'NIST', color: 'orange' },
    { value: 'SBS', label: 'SBS Perú', color: 'teal' }
  ];

  return (
    <Box p={4} borderWidth={1} borderRadius="md" bg="gray.50">
      <Text fontWeight="bold" mb={3}>{t.ui.reports.filters.filters_by_standard}</Text>
      
      <VStack align="start" spacing={2}>
        <Box w="full">
          <Text fontSize="sm" fontWeight="medium" mb={2}>{t.ui.reports.filters.security_standards}</Text>
          <VStack spacing={1}>
            {standardsData
              .filter(standard => availableStandards.includes(standard.value))
              .map((standard) => (
                <Button
                  key={standard.value}
                  size="sm"
                  variant={selectedStandards.includes(standard.value) ? "solid" : "outline"}
                  colorScheme={selectedStandards.includes(standard.value) ? standard.color : "gray"}
                  onClick={() => onStandardToggle(standard.value)}
                  w="full"
                  justifyContent="center"
                >
                  {standard.label}
                </Button>
              ))}
          </VStack>
        </Box>

        {/* Mostrar estándares seleccionados */}
        {selectedStandards.length > 0 && (
          <Box w="full" mt={2}>
            <Text fontSize="xs" color="gray.600" mb={1}>{t.ui.reports.filters.active_filters}:</Text>
            <HStack spacing={1} wrap="wrap">
              {selectedStandards.map((standard) => {
                const standardData = standardsData.find(s => s.value === standard);
                return (
                  <Badge 
                    key={standard} 
                    colorScheme={standardData?.color || 'gray'} 
                    size="sm"
                    cursor="pointer"
                    onClick={() => onStandardToggle(standard)}
                  >
                    {standardData?.label || standard} ✕
                  </Badge>
                );
              })}
            </HStack>
          </Box>
        )}
      </VStack>
    </Box>
  );
};

/**
 * Componente RiskFilter
 * Filtro por niveles de riesgo inherente y actual
 */
const RiskFilter = ({ 
  selectedInherentRisk, 
  selectedCurrentRisk,
  onInherentRiskChange,
  onCurrentRiskChange
}) => {
  const { t } = useLocalization();
  
  const riskLevels = [
    { value: 'LOW', label: t.ui.reports.filters.risk_levels.low, color: 'green' },
    { value: 'MEDIUM', label: t.ui.reports.filters.risk_levels.medium, color: 'yellow' },
    { value: 'HIGH', label: t.ui.reports.filters.risk_levels.high, color: 'orange' },
    { value: 'CRITICAL', label: t.ui.reports.filters.risk_levels.critical, color: 'red' }
  ];

  return (
    <Box p={4} borderWidth={1} borderRadius="md" bg="gray.50">
      <Text fontWeight="bold" mb={3}>{t.ui.reports.filters.filters_by_risk}</Text>
      
      {/* Filtro por Riesgo Inherente */}
      <VStack align="start" spacing={3}>
        <Box w="full">
          <Text fontSize="sm" fontWeight="medium" mb={2}>{t.ui.reports.inherent_risk}</Text>
          <VStack spacing={1}>
            {riskLevels.map((level) => (
              <Button
                key={`inherit-${level.value}`}
                size="sm"
                variant={selectedInherentRisk === level.value ? "solid" : "outline"}
                colorScheme={selectedInherentRisk === level.value ? level.color : "gray"}
                onClick={() => onInherentRiskChange(
                  selectedInherentRisk === level.value ? null : level.value
                )}
                w="full"
                justifyContent="center"
              >
                {level.label}
              </Button>
            ))}
          </VStack>
        </Box>

        {/* Filtro por Riesgo Actual */}
        <Box w="full">
          <Text fontSize="sm" fontWeight="medium" mb={2}>{t.ui.reports.current_risk}</Text>
          <VStack spacing={1}>
            {riskLevels.map((level) => (
              <Button
                key={`current-${level.value}`}
                size="sm"
                variant={selectedCurrentRisk === level.value ? "solid" : "outline"}
                colorScheme={selectedCurrentRisk === level.value ? level.color : "gray"}
                onClick={() => onCurrentRiskChange(
                  selectedCurrentRisk === level.value ? null : level.value
                )}
                w="full"
                justifyContent="center"
              >
                {level.label}
              </Button>
            ))}
          </VStack>
        </Box>

        {/* Mostrar filtros de riesgo activos */}
        {(selectedInherentRisk || selectedCurrentRisk) && (
          <Box w="full" mt={2}>
            <Text fontSize="xs" color="gray.600" mb={1}>{t.ui.reports.filters.active_filters}:</Text>
            <HStack spacing={1} wrap="wrap">
              {selectedInherentRisk && (
                <Badge 
                  colorScheme={riskLevels.find(r => r.value === selectedInherentRisk)?.color || 'gray'} 
                  size="sm"
                  cursor="pointer"
                  onClick={() => onInherentRiskChange(null)}
                >
                  {t.ui.reports.filters.inherent}: {riskLevels.find(r => r.value === selectedInherentRisk)?.label} ✕
                </Badge>
              )}
              {selectedCurrentRisk && (
                <Badge 
                  colorScheme={riskLevels.find(r => r.value === selectedCurrentRisk)?.color || 'gray'} 
                  size="sm"
                  cursor="pointer"
                  onClick={() => onCurrentRiskChange(null)}
                >
                  {t.ui.reports.filters.current}: {riskLevels.find(r => r.value === selectedCurrentRisk)?.label} ✕
                </Badge>
              )}
            </HStack>
          </Box>
        )}
      </VStack>
    </Box>
  );
};

/**
 * Componente principal ReportsFilters
 * Panel completo de filtros para reportes
 */
const ReportsFilters = ({
  selectedStandards,
  onStandardToggle,
  availableStandards,
  selectedInherentRisk,
  selectedCurrentRisk,
  onInherentRiskChange,
  onCurrentRiskChange,
  onClearAllFilters
}) => {
  const { t } = useLocalization();

  const hasActiveFilters = selectedStandards.length > 0 || selectedInherentRisk || selectedCurrentRisk;

  return (
    <Box minW="250px">
      <VStack spacing={4}>
        <StandardsFilter
          selectedStandards={selectedStandards}
          onStandardToggle={onStandardToggle}
          availableStandards={availableStandards}
        />
        
        <RiskFilter
          selectedInherentRisk={selectedInherentRisk}
          selectedCurrentRisk={selectedCurrentRisk}
          onInherentRiskChange={onInherentRiskChange}
          onCurrentRiskChange={onCurrentRiskChange}
        />
      </VStack>
      
      {/* Botón para limpiar filtros */}
      {hasActiveFilters && (
        <Box mt={4}>
          <Button
            size="sm"
            variant="outline"
            colorScheme="gray"
            onClick={onClearAllFilters}
            width="full"
          >
            {t.ui.reports.filters.clear_all_filters}
          </Button>
        </Box>
      )}
    </Box>
  );
};

export default ReportsFilters;
