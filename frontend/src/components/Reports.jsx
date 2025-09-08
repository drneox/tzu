/**
 * Componente Reports
 * Muestra todas las amenazas de todos los sistemas con capacidad de filtrado
 */
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Box,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  HStack,
  VStack,
  Text,
  Badge,
  Alert,
  AlertIcon,
  Spinner,
  Center,
  Flex,
  IconButton,
  Button,
  Collapse
} from '@chakra-ui/react';
import { ChevronLeftIcon, ChevronRightIcon, ViewIcon, ViewOffIcon } from '@chakra-ui/icons';
import { useLocalization } from '../hooks/useLocalization';
import { getAllThreats } from '../services';
import ReportsFilters from './ReportsFilters';

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
 * Componente principal Reports
 */
const Reports = () => {
  const { t } = useLocalization();
  const [threats, setThreats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedStandards, setSelectedStandards] = useState([]);
  const [availableStandards] = useState(['ASVS', 'MASVS', 'NIST', 'ISO27001', 'SBS']);
  
  // Estados para filtros de riesgo
  const [selectedInherentRisk, setSelectedInherentRisk] = useState(null);
  const [selectedCurrentRisk, setSelectedCurrentRisk] = useState(null);

  // Estados de paginación
  const [currentPage, setCurrentPage] = useState(1);
  const [threatsPerPage] = useState(20);

  // Estado para controlar la visibilidad del panel de filtros
  const [showFilters, setShowFilters] = useState(true);

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
      
      // DEBUG: Ver estructura completa de datos
      if (threatsArray.length > 0) {
        console.log('=== ESTRUCTURA COMPLETA DE AMENAZA ===');
        console.log('Amenaza completa:', JSON.stringify(threatsArray[0], null, 2));
        console.log('Information system keys:', Object.keys(threatsArray[0].information_system || {}));
        console.log('Information system:', threatsArray[0].information_system);
        console.log('Information system ID:', threatsArray[0].information_system?.id);
        console.log('Information system title:', threatsArray[0].information_system?.title);
      }
      
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
      filters.standards = selectedStandards; // Pasar como array, no como string
    }
    
    if (selectedInherentRisk) {
      filters.inherit_risk = selectedInherentRisk;
    }
    
    if (selectedCurrentRisk) {
      filters.current_risk = selectedCurrentRisk;
    }
    
    loadThreats(filters);
  }, [selectedStandards, selectedInherentRisk, selectedCurrentRisk]);

  // Manejar toggle de estándares
  const handleStandardToggle = (standard) => {
    setSelectedStandards(prev => 
      prev.includes(standard)
        ? prev.filter(s => s !== standard)
        : [...prev, standard]
    );
  };

  // Manejar cambios en filtros de riesgo
  const handleInherentRiskChange = (riskLevel) => {
    setSelectedInherentRisk(riskLevel);
  };

  const handleCurrentRiskChange = (riskLevel) => {
    setSelectedCurrentRisk(riskLevel);
  };

  // Función para limpiar todos los filtros
  const handleClearAllFilters = () => {
    setSelectedStandards([]);
    setSelectedInherentRisk(null);
    setSelectedCurrentRisk(null);
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
          <Text>{t.ui.reports.loading_threats}</Text>
        </VStack>
      </Center>
    );
  }

  if (error) {
    return (
      <Alert status="error">
        <AlertIcon />
        {t.ui.reports.error_loading}: {error}
      </Alert>
    );
  }

  return (
    <Box p={6} maxW="100vw" overflow="hidden">
      <Flex justify="space-between" align="center" mb={6}>
        <Heading size="lg">
          {t.ui.reports.title}
        </Heading>
      </Flex>

      <Box maxW="100%" overflow="hidden">
        <Flex direction="row" align="start" gap={6} maxW="100%">
        {/* Panel de filtros lateral con Collapse */}
        <Collapse in={showFilters} axis="x" animateOpacity>
          <Box
            minW="280px"
            maxW="280px" 
            p={4} 
            borderWidth="1px" 
            borderRadius="md" 
            bg="gray.50"
            h="fit-content"
          >
            <ReportsFilters
              selectedStandards={selectedStandards}
              onStandardToggle={handleStandardToggle}
              availableStandards={availableStandards}
              selectedInherentRisk={selectedInherentRisk}
              selectedCurrentRisk={selectedCurrentRisk}
              onInherentRiskChange={handleInherentRiskChange}
              onCurrentRiskChange={handleCurrentRiskChange}
              onClearAllFilters={handleClearAllFilters}
            />
          </Box>
        </Collapse>

        {/* Tabla de amenazas */}
        <Box flex={1} minW={0}>
          <VStack align="start" spacing={4}>
            <Flex justify="space-between" align="center" w="full">
              {/* Botón para mostrar/ocultar filtros */}
              <Button
                leftIcon={showFilters ? <ViewOffIcon /> : <ViewIcon />}
                onClick={() => setShowFilters(!showFilters)}
                variant="outline"
                size="sm"
                colorScheme="blue"
                position="relative"
              >
                {showFilters ? t.ui.reports.hide_filters : t.ui.reports.show_filters}
                {/* Indicador de filtros activos cuando están ocultos */}
                {!showFilters && (selectedStandards.length > 0 || selectedInherentRisk || selectedCurrentRisk) && (
                  <Box
                    position="absolute"
                    top="-2px"
                    right="-2px"
                    w="8px"
                    h="8px"
                    bg="red.500"
                    borderRadius="full"
                    border="2px solid white"
                  />
                )}
              </Button>

              <Text fontSize="sm" color="gray.600">
                {t.ui.reports.showing_page} {currentPage} - {currentThreats.length} {t.ui.reports.threats}
                {(selectedStandards.length > 0 || selectedInherentRisk || selectedCurrentRisk) && (
                  <Text as="span" ml={2} color="blue.600">
                    ({t.ui.reports.filtered_by}: {[
                      ...(selectedStandards.length > 0 ? [`${t.ui.reports.standards}: ${selectedStandards.join(', ')}`] : []),
                      ...(selectedInherentRisk ? [`${t.ui.reports.inherent_risk}: ${selectedInherentRisk}`] : []),
                      ...(selectedCurrentRisk ? [`${t.ui.reports.current_risk}: ${selectedCurrentRisk}`] : [])
                    ].join(' | ')})
                  </Text>
                )}
                {!showFilters && (selectedStandards.length > 0 || selectedInherentRisk || selectedCurrentRisk) && (
                  <Text as="span" ml={2} color="orange.600" fontSize="xs">
                    • {t.ui.reports.active_filters_hidden}
                  </Text>
                )}
              </Text>
            </Flex>

            <Table variant="simple" size="sm">
              <Thead>
                <Tr>
                  <Th>{t.ui.reports.threat_modelling}</Th>
                  <Th>{t.ui.description}</Th>
                  <Th>{t.ui.type}</Th>
                  <Th>{t.ui.reports.inherent_risk}</Th>
                  <Th>{t.ui.reports.current_risk}</Th>
                  <Th>{t.ui.reports.residual_risk}</Th>
                  <Th>{t.ui.reports.tags}</Th>
                </Tr>
              </Thead>
              <Tbody>
                {Array.isArray(currentThreats) && currentThreats.length > 0 ? (
                  currentThreats.map((threat) => {
                    const inheritRisk = threat.risk?.inherit_risk || 'N/A';
                    const currentRiskLevel = threat.current_risk_level || 'N/A';
                    const residualRisk = threat.risk?.residual_risk || null;
                    
                    // Debug: Ver datos del sistema
                    if (threat.information_system) {
                      console.log('Sistema encontrado:', {
                        id: threat.information_system.id,
                        title: threat.information_system.title,
                        hasId: !!threat.information_system.id
                      });
                    } else {
                      console.log('Sin sistema de información para amenaza:', threat.id);
                    }
                    
                    const getRiskBadgeColor = (risk) => {
                      switch(risk) {
                        case 'LOW': return 'green';
                        case 'MEDIUM': return 'yellow';
                        case 'HIGH': return 'orange';
                        case 'CRITICAL': return 'red';
                        default: return 'gray';
                      }
                    };

                    const getRiskLevelFromScore = (score) => {
                      if (score === null || score === undefined) return null;
                      if (score <= 3) return 'LOW';
                      if (score <= 6) return 'MEDIUM';
                      return 'HIGH';
                    };
                    
                    return (
                      <Tr key={threat.id}>
                        <Td>
                          {threat.information_system?.title && threat.information_system?.id ? (
                            <Link to={`/analysis/${threat.information_system.id}`}>
                              <Text fontWeight="medium" fontSize="sm" color="blue.600" _hover={{ textDecoration: 'underline' }}>
                                {threat.information_system.title}
                              </Text>
                            </Link>
                          ) : (
                            <Text fontWeight="medium" fontSize="sm" color="gray.500">
                              N/A
                            </Text>
                          )}
                        </Td>
                        <Td>
                          <Text fontWeight="medium" fontSize="sm">
                            {threat.title}
                          </Text>
                        </Td>
                        <Td>
                          <Badge colorScheme="blue" size="sm">
                            {threat.type}
                          </Badge>
                        </Td>
            
                        <Td>
                          <Badge 
                            colorScheme={getRiskBadgeColor(inheritRisk)} 
                            size="sm"
                          >
                            {inheritRisk}
                          </Badge>
                        </Td>
                        <Td>
                          <Badge 
                            colorScheme={getRiskBadgeColor(currentRiskLevel)} 
                            size="sm"
                          >
                            {currentRiskLevel}
                          </Badge>
                        </Td>
                        <Td>
                          {residualRisk !== null ? (
                            <Badge 
                              colorScheme={getRiskBadgeColor(getRiskLevelFromScore(residualRisk))} 
                              size="sm"
                            >
                              {getRiskLevelFromScore(residualRisk)}
                            </Badge>
                          ) : (
                            <Text fontSize="sm" color="gray.500">N/A</Text>
                          )}
                        </Td>
                        <Td>
                          <HStack spacing={1} wrap="wrap">
                            {Array.isArray(threat.remediation?.control_tags) && threat.remediation.control_tags.length > 0 ? (
                              threat.remediation.control_tags.map((tag, index) => (
                                <Badge key={index} colorScheme="gray" size="sm">
                                  {tag}
                                </Badge>
                              ))
                            ) : (
                              <Text fontSize="sm" color="gray.500">{t.ui.reports.no_tags}</Text>
                            )}
                          </HStack>
                        </Td>
                      </Tr>
                    );
                  })
                ) : (
                  <Tr>
                    <Td colSpan={7} textAlign="center">
                      <Text color="gray.500">{t.ui.reports.no_threats}</Text>
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
                  aria-label={t.ui.reports.previous_page}
                />
                
                <Text fontSize="sm">
                  {t.ui.reports.page} {currentPage}
                </Text>
                
                <IconButton
                  icon={<ChevronRightIcon />}
                  onClick={nextPage}
                  isDisabled={currentThreats.length < threatsPerPage}
                  size="sm"
                  aria-label={t.ui.reports.next_page}
                />
              </Flex>
            )}
          </VStack>
        </Box>
      </Flex>
      </Box>
    </Box>
  );
};

export default Reports;
