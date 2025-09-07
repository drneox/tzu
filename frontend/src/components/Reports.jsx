/**
 * Componente Reports
} from '@chakra-ui/react';
import { ChevronLeftIcon, ChevronRightIcon } from '@chakra-ui/icons';
import { useLocalization } from '../hooks/useLocalization';
import { getAllThreats } from '../services/index';estra todas las amenazas de todos los sistemas con capacidad de filtrado
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
  HStack,
  VStack,
  Text,
  Badge,
  useDisclosure,
  Alert,
  AlertIcon,
  Spinner,
  Center,
  Flex,
  IconButton
} from '@chakra-ui/react';
import { ChevronLeftIcon, ChevronRightIcon } from '@chakra-ui/icons';
import { useLocalization } from '../hooks/useLocalization';
import useTagCategorization from '../hooks/useTagCategorization';
import { getAllThreats } from '../services';

/**
 * Componente para mostrar el valor de riesgo con color
 */
const RiskDisplay = ({ value, type = "current" }) => {
  const getRiskColor = (risk) => {
    if (risk <= 3) return "green";
    if (risk <= 6) return "yellow";
    return "red";
  };

  const getRiskText = (risk) => {
    if (risk <= 3) return "Bajo";
    if (risk <= 6) return "Medio";
    return "Alto";
  };

  return (
    <Badge colorScheme={getRiskColor(value)} size="lg" px={2} py={1}>
      {value.toFixed(1)} - {getRiskText(value)}
    </Badge>
  );
};

/**
 * Componente StandardsFilter
 * Filtro por estándares de control tags (simplificado para backend)
 */
const StandardsFilter = ({ 
  selectedStandards, 
  onStandardToggle,
  availableStandards
}) => {
  const { t } = useLocalization();

  const standardNames = {
    "ASVS": "ASVS",
    "MASVS": "MASVS", 
    "ISO27001": "ISO 27001",
    "NIST": "NIST",
    "SBS": "SBS Perú"
  };

  return (
    <Box p={4} borderWidth={1} borderRadius="md" bg="gray.50">
      <Text fontWeight="bold" mb={2}>Filtros por Estándar</Text>
      <VStack align="start" spacing={2}>
        {availableStandards.map((standard) => (
          <HStack key={standard} justify="space-between" w="full">
            <Button
              size="sm"
              variant={selectedStandards.includes(standard) ? "solid" : "outline"}
              colorScheme={selectedStandards.includes(standard) ? "blue" : "gray"}
              onClick={() => onStandardToggle(standard)}
              flex={1}
              justifyContent="center"
            >
              <Text>{standardNames[standard]}</Text>
            </Button>
          </HStack>
        ))}
      </VStack>
    </Box>
  );
};

/**
 * Componente principal Reports
 */
const Reports = () => {
  const { t } = useLocalization();
  const [threats, setThreats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedStandards, setSelectedStandards] = useState([]);
  const [availableStandards] = useState(['ASVS', 'MASVS', 'NIST', 'ISO27001', 'SBS']);

  // Estados de paginación
  const [currentPage, setCurrentPage] = useState(1);
  const [threatsPerPage] = useState(20);

  // Función para cargar amenazas (con filtros opcionales)
  const loadThreats = async (filters = {}) => {
    try {
      setLoading(true);
      setError(null);
      
      const params = {
        skip: (currentPage - 1) * threatsPerPage,
        limit: threatsPerPage,
        ...filters
      };
      
      const result = await getAllThreats(params);
      const threatsArray = Array.isArray(result) ? result : [];
      
      // El backend ya devuelve las amenazas filtradas y ordenadas
      setThreats(threatsArray);
      
    } catch (err) {
      setError(err.message);
      setThreats([]);
    } finally {
      setLoading(false);
    }
  };

  // Cargar amenazas al montar el componente
  useEffect(() => {
    loadThreats();
  }, [currentPage]);

  // Recargar cuando cambian los filtros
  useEffect(() => {
    setCurrentPage(1); // Resetear a la primera página
    const filters = {};
    
    if (selectedStandards.length > 0) {
      filters.standards = selectedStandards;
    }
    
    loadThreats(filters);
  }, [selectedStandards]);

  // Manejar toggle de estándares
  const handleStandardToggle = (standard) => {
    setSelectedStandards(prev => 
      prev.includes(standard)
        ? prev.filter(s => s !== standard)
        : [...prev, standard]
    );
  };

  // Simplificar paginación - el backend ya maneja skip/limit
  const currentThreats = Array.isArray(threats) ? threats : [];

  const nextPage = () => {
    setCurrentPage(prev => prev + 1);
  };

  const prevPage = () => {
    setCurrentPage(prev => Math.max(prev - 1, 1));
  };

  // Calcular riesgo actual
  const calculateCurrentRisk = (risk) => {
    if (!risk) return 0;
    
    const threatAgentFactors = (risk.skill_level + risk.motive + risk.opportunity + risk.size) / 4;
    const vulnerabilityFactors = (risk.ease_of_discovery + risk.ease_of_exploit + risk.awareness + risk.intrusion_detection) / 4;
    const likelihood = (threatAgentFactors + vulnerabilityFactors) / 2;
    
    const technicalImpact = (risk.loss_of_confidentiality + risk.loss_of_integrity + risk.loss_of_availability + risk.loss_of_accountability) / 4;
    const businessImpact = (risk.financial_damage + risk.reputation_damage + risk.non_compliance + risk.privacy_violation) / 4;
    const impact = (technicalImpact + businessImpact) / 2;
    
    return (likelihood + impact) / 2;
  };

  if (loading) {
    return (
      <Center h="400px">
        <VStack>
          <Spinner size="xl" />
          <Text>Cargando amenazas...</Text>
        </VStack>
      </Center>
    );
  }

  if (error) {
    return (
      <Alert status="error">
        <AlertIcon />
        Error al cargar las amenazas: {error}
      </Alert>
    );
  }

  return (
    <Box p={6}>
      <Heading size="lg" mb={6}>
        {t.ui.menu.reports || "Reportes"} - Todas las Amenazas
      </Heading>

      <HStack align="start" spacing={6}>
        {/* Panel de filtros */}
        <Box minW="250px">
          <StandardsFilter
            selectedStandards={selectedStandards}
            onStandardToggle={handleStandardToggle}
            availableStandards={availableStandards}
          />
          
          {/* Botón para limpiar filtros */}
          {selectedStandards.length > 0 && (
            <Box mt={4}>
              <Button
                size="sm"
                variant="outline"
                colorScheme="gray"
                onClick={() => setSelectedStandards([])}
                width="full"
              >
                Limpiar filtros
              </Button>
            </Box>
          )}
        </Box>

        {/* Tabla de amenazas */}
        <Box flex={1}>
          <VStack align="start" spacing={4}>
            <Text fontSize="sm" color="gray.600">
              Mostrando página {currentPage} - {currentThreats.length} amenazas
              {selectedStandards.length > 0 && (
                <Text as="span" ml={2} color="blue.600">
                  (Filtrado por: {selectedStandards.join(', ')})
                </Text>
              )}
            </Text>

            <Table variant="simple" size="sm">
              <Thead>
                <Tr>
                  <Th>Sistema</Th>
                  <Th>Tipo</Th>
                  <Th>Título</Th>
                  <Th>Descripción</Th>
                  <Th>Riesgo Actual</Th>
                  <Th>Riesgo Residual</Th>
                  <Th>Tags</Th>
                </Tr>
              </Thead>
              <Tbody>
                {Array.isArray(currentThreats) && currentThreats.length > 0 ? (
                  currentThreats.map((threat) => {
                    const currentRisk = calculateCurrentRisk(threat.risk);
                    const residualRisk = threat.risk?.residual_risk || 0;      
                    return (
                      <Tr key={threat.id}>
                        <Td>
                          <Text fontWeight="medium" fontSize="sm">
                            {threat.information_system?.title || 'N/A'}
                          </Text>
                        </Td>
                        <Td>
                          <Badge colorScheme="purple" size="sm">
                            {threat.type}
                          </Badge>
                        </Td>
                        <Td>
                          <Text fontWeight="medium" fontSize="sm">
                            {threat.title}
                          </Text>
                        </Td>
                        <Td maxW="300px">
                          <Text fontSize="sm" noOfLines={2}>
                            {threat.description}
                          </Text>
                        </Td>
                        <Td>
                          <RiskDisplay value={currentRisk} type="current" />
                        </Td>
                        <Td>
                          {residualRisk > 0 ? (
                            <RiskDisplay value={residualRisk} type="residual" />
                          ) : (
                            <Text fontSize="sm" color="gray.500">N/A</Text>
                          )}
                        </Td>
                        <Td>
                          <HStack wrap="wrap" spacing={1}>
                            {(threat.remediation?.control_tags || []).slice(0, 3).map((tag, index) => (
                              <Badge key={index} size="xs" variant="outline">
                                {tag}
                              </Badge>
                            ))}
                            {(threat.remediation?.control_tags?.length || 0) > 3 && (
                              <Badge size="xs" colorScheme="gray">
                                +{(threat.remediation?.control_tags?.length || 0) - 3}
                              </Badge>
                            )}
                          </HStack>
                        </Td>
                      </Tr>
                    );
                  })
                ) : (
                  <Tr>
                    <Td colSpan={8} textAlign="center" py={8}>
                      <Text color="gray.500">
                        {selectedStandards.length > 0 
                          ? `No se encontraron amenazas para los estándares seleccionados: ${selectedStandards.join(', ')}`
                          : 'No hay amenazas disponibles'
                        }
                      </Text>
                    </Td>
                  </Tr>
                )}
              </Tbody>
            </Table>

            {/* Controles de paginación */}
            {currentThreats.length === threatsPerPage && (
              <Flex justify="center" align="center" mt={4} gap={4}>
                <IconButton
                  icon={<ChevronLeftIcon />}
                  onClick={prevPage}
                  isDisabled={currentPage === 1}
                  size="sm"
                  aria-label="Página anterior"
                />
                
                <Text fontSize="sm">
                  Página {currentPage}
                </Text>
                
                <IconButton
                  icon={<ChevronRightIcon />}
                  onClick={nextPage}
                  isDisabled={currentThreats.length < threatsPerPage}
                  size="sm"
                  aria-label="Página siguiente"
                />
              </Flex>
            )}
          </VStack>
        </Box>
      </HStack>
    </Box>
  );
};

export default Reports;
