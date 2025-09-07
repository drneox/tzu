import React, { useState, useEffect } from 'react';
import {
  Box,
  VStack,
  HStack,
  Text,
  Button,
  Badge,
  Card,
  CardHeader,
  CardBody,
  Checkbox,
  CheckboxGroup,
  Collapse,
  IconButton,
  useDisclosure,
  Spinner,
  Alert,
  AlertIcon,
  Divider,
  Tooltip,
  useColorModeValue
} from '@chakra-ui/react';
import { FaFilter, FaTimes, FaChevronDown, FaChevronUp } from 'react-icons/fa';
import { fetchAvailableStandards, fetchControlTagsHierarchy } from '../services/index';
import { useLocalization } from '../hooks/useLocalization';
import useTagCategorization from '../hooks/useTagCategorization';

const StandardsFilter = ({ 
  onFiltersChange, 
  selectedStandards = [], 
  threats = [],
  showCounts = true 
}) => {
  const { t } = useLocalization();
  const { isOpen, onToggle } = useDisclosure();
  
  // Estados
  const [standards, setStandards] = useState([]);
  const [hierarchy, setHierarchy] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [threatCounts, setThreatCounts] = useState({});
  
  // Hook para categorización de tags
  const { countThreatsWithStandard } = useTagCategorization();
  
  // Color mode
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  
  // Cargar datos iniciales
  useEffect(() => {
    const loadFilterData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Cargar estándares y jerarquía en paralelo
        const [standardsResponse, hierarchyResponse] = await Promise.all([
          fetchAvailableStandards(),
          fetchControlTagsHierarchy()
        ]);
        
        setStandards(standardsResponse.standards || []);
        setHierarchy(hierarchyResponse);
        
      } catch (err) {
        console.error('Error loading filter data:', err);
        setError(err.message || 'Error al cargar datos de filtrado');
      } finally {
        setLoading(false);
      }
    };
    
    loadFilterData();
  }, []);
  
  // Efecto para actualizar conteos cuando cambian las amenazas
  useEffect(() => {
    const updateThreatCounts = async () => {
      if (!showCounts || !standards.length || !threats.length) {
        setThreatCounts({});
        return;
      }

      try {
        const counts = {};
        for (const standard of standards) {
          counts[standard] = await countThreatsWithStandard(threats, standard);
        }
        setThreatCounts(counts);
      } catch (error) {
        console.error('Error updating threat counts:', error);
        setThreatCounts({});
      }
    };

    updateThreatCounts();
  }, [threats, standards, showCounts, countThreatsWithStandard]);
  
  // Función para obtener el conteo de amenazas para un estándar (desde estado)
  const getThreatCountForStandard = (standardName) => {
    return threatCounts[standardName] || 0;
  };
  
  // Función para obtener total de controles por estándar desde la jerarquía
  const getTotalControlsForStandard = (standardName) => {
    if (!hierarchy || !hierarchy.standards) return 0;
    
    const standardData = hierarchy.standards[standardName];
    if (!standardData) return 0;
    
    return standardData.total_controls || 0;
  };
  
  // Manejar cambios en la selección de estándares
  const handleStandardChange = (newSelectedStandards) => {
    onFiltersChange({
      selectedStandards: newSelectedStandards,
      activeFilters: newSelectedStandards.length > 0
    });
  };
  
  // Limpiar todos los filtros
  const clearAllFilters = () => {
    handleStandardChange([]);
  };
  
  // Función para verificar si hay filtros activos
  const hasActiveFilters = selectedStandards.length > 0;
  
  if (loading) {
    return (
      <Card bg={cardBg} border="1px" borderColor={borderColor}>
        <CardBody>
          <HStack>
            <Spinner size="sm" />
            <Text>Cargando filtros...</Text>
          </HStack>
        </CardBody>
      </Card>
    );
  }
  
  if (error) {
    return (
      <Alert status="error" borderRadius="md">
        <AlertIcon />
        <Text fontSize="sm">{error}</Text>
      </Alert>
    );
  }
  
  return (
    <Card bg={cardBg} border="1px" borderColor={borderColor}>
      <CardHeader pb={2}>
        <HStack justify="space-between">
          <HStack>
            <FaFilter />
            <Text fontWeight="bold" fontSize="md">
              Filtrar por Estándares
            </Text>
            {hasActiveFilters && (
              <Badge colorScheme="blue" variant="solid">
                {selectedStandards.length}
              </Badge>
            )}
          </HStack>
          
          <HStack spacing={2}>
            {hasActiveFilters && (
              <Tooltip label="Limpiar filtros">
                <IconButton
                  size="sm"
                  variant="ghost"
                  icon={<FaTimes />}
                  onClick={clearAllFilters}
                  aria-label="Limpiar filtros"
                />
              </Tooltip>
            )}
            
            <IconButton
              size="sm"
              variant="ghost"
              icon={isOpen ? <FaChevronUp /> : <FaChevronDown />}
              onClick={onToggle}
              aria-label={isOpen ? "Contraer" : "Expandir"}
            />
          </HStack>
        </HStack>
      </CardHeader>
      
      <Collapse in={isOpen} animateOpacity>
        <CardBody pt={0}>
          {standards.length === 0 ? (
            <Text fontSize="sm" color="gray.500">
              No se encontraron estándares disponibles
            </Text>
          ) : (
            <VStack align="stretch" spacing={3}>
              <Text fontSize="sm" color="gray.600">
                Selecciona uno o más estándares para filtrar amenazas con controles asociados:
              </Text>
              
              <CheckboxGroup
                value={selectedStandards}
                onChange={handleStandardChange}
              >
                <VStack align="stretch" spacing={2}>
                  {standards.map(standard => {
                    const threatCount = showCounts ? getThreatCountForStandard(standard) : 0;
                    const totalControls = getTotalControlsForStandard(standard);
                    
                    return (
                      <HStack key={standard} justify="space-between">
                        <Checkbox value={standard} size="md">
                          <Text fontWeight="medium">{standard}</Text>
                        </Checkbox>
                        
                        {showCounts && (
                          <HStack spacing={1}>
                            {threatCount > 0 && (
                              <Tooltip label={`${threatCount} amenaza${threatCount !== 1 ? 's' : ''} con controles ${standard}`}>
                                <Badge colorScheme="green" variant="subtle" size="sm">
                                  {threatCount}
                                </Badge>
                              </Tooltip>
                            )}
                            {totalControls > 0 && (
                              <Tooltip label={`${totalControls} controles disponibles en ${standard}`}>
                                <Badge colorScheme="blue" variant="outline" size="sm">
                                  {totalControls}
                                </Badge>
                              </Tooltip>
                            )}
                          </HStack>
                        )}
                      </HStack>
                    );
                  })}
                </VStack>
              </CheckboxGroup>
              
              {hasActiveFilters && (
                <>
                  <Divider />
                  <VStack align="stretch" spacing={2}>
                    <Text fontSize="sm" fontWeight="medium" color="blue.600">
                      Filtros activos:
                    </Text>
                    <HStack wrap="wrap" spacing={1}>
                      {selectedStandards.map(standard => (
                        <Badge 
                          key={standard} 
                          colorScheme="blue" 
                          variant="solid"
                          display="flex"
                          alignItems="center"
                          gap={1}
                        >
                          {standard}
                          <IconButton
                            size="xs"
                            variant="ghost"
                            color="white"
                            icon={<FaTimes />}
                            onClick={() => {
                              const newSelected = selectedStandards.filter(s => s !== standard);
                              handleStandardChange(newSelected);
                            }}
                            aria-label={`Quitar filtro ${standard}`}
                            _hover={{ bg: 'whiteAlpha.300' }}
                          />
                        </Badge>
                      ))}
                    </HStack>
                  </VStack>
                </>
              )}
            </VStack>
          )}
        </CardBody>
      </Collapse>
    </Card>
  );
};

export default StandardsFilter;
