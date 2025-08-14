import axios from "axios";
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { FaTrash, FaFilePdf, FaEdit, FaEye, FaChevronDown, FaChevronUp, FaTable, FaThLarge, FaEyeSlash } from "react-icons/fa";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Flex, TableContainer, Table, Tr, Td, Thead, Th, Tbody, Card, CardHeader, CardBody, Grid, GridItem, Text, Image as ChakraImage, Modal, ModalOverlay, ModalContent, ModalCloseButton, ModalBody, useDisclosure, Button, Icon, useToast, Tabs, TabList, TabPanels, Tab, TabPanel, Accordion, AccordionItem, AccordionButton, AccordionPanel, AccordionIcon, VStack, HStack, Divider, Badge, Collapse, useColorModeValue, Box, Tooltip, Switch, FormControl, FormLabel } from "@chakra-ui/react";
import { fetchInformationSystemById, updateThreatsRiskBatch, createThreatForSystem, updateThreatResidualRisk, updateThreatsResidualRiskBatch } from "../services/index";
import { useLocalization, getOwaspSelectOptions } from '../hooks/useLocalization';
import OwaspSelector from './OwaspSelector';
import ReportGenerator from './ReportGenerator';

// Función para calcular la altura del textarea basada en el contenido
const calculateTextareaHeight = (text, width) => {
  const lineHeight = 20; // altura de línea en px
  const padding = 8; // padding vertical
  const baseHeight = 40; // altura mínima
  
  if (!text) return baseHeight;
  
  // Estimar el número de líneas basado en la longitud del texto y el ancho
  const averageCharsPerLine = Math.floor(width / 8); // aproximadamente 8px por carácter
  const estimatedLines = Math.ceil(text.length / averageCharsPerLine);
  const newLines = (text.match(/\n/g) || []).length;
  
  const totalLines = Math.max(estimatedLines, newLines + 1);
  const calculatedHeight = Math.max(baseHeight, totalLines * lineHeight + padding * 2);
  
  return Math.min(calculatedHeight, 120); // máximo 120px de altura
};

// Función para auto-redimensionar textarea cuando el usuario escribe
const handleTextareaResize = (event) => {
  const textarea = event.target;
  textarea.style.height = 'auto';
  textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
};

// Función para calcular el riesgo inherente usando OWASP Risk Rating completo
const calculateInherentRisk = (risk) => {
  if (!risk) return 0;
  
  // OWASP Risk Rating: (Likelihood + Impact) / 2
  const likelihoodFactors = [
    // Threat Agent Factors
    risk.skill_level || 0,
    risk.motive || 0,
    risk.opportunity || 0,
    risk.size || 0,
    // Vulnerability Factors
    risk.ease_of_discovery || 0,
    risk.ease_of_exploit || 0,
    risk.awareness || 0,
    risk.intrusion_detection || 0
  ];
  
  const impactFactors = [
    // Technical Impact
    risk.loss_of_confidentiality || 0,
    risk.loss_of_integrity || 0,
    risk.loss_of_availability || 0,
    risk.loss_of_accountability || 0,
    // Business Impact
    risk.financial_damage || 0,
    risk.reputation_damage || 0,
    risk.non_compliance || 0,
    risk.privacy_violation || 0
  ];
  
  const likelihood = likelihoodFactors.reduce((acc, val) => acc + val, 0) / likelihoodFactors.length;
  const impact = impactFactors.reduce((acc, val) => acc + val, 0) / impactFactors.length;
  
  const overallRisk = (likelihood + impact) / 2;
  return overallRisk.toFixed(2);
};

// Función para calcular el riesgo residual basado en el riesgo inherente y la remediación

// Función para obtener el color del riesgo inherente según OWASP Risk Rating Scale
// Esta función ha sido reemplazada por la definida dentro del componente

// Función para obtener el label del riesgo según OWASP
const getRiskLabel = (riskValue, t) => {
  const value = parseFloat(riskValue);
  if (value < 3) return t?.ui?.risk_low || "LOW";
  if (value < 6) return t?.ui?.risk_medium || "MEDIUM"; 
  return t?.ui?.risk_high || "HIGH";
};

const Analysis = () => {
  const [isLoading, setIsLoading] = useState(true);
  const { id } = useParams();
  const [serviceData, setServiceData] = useState(null);
  const [threats, setThreats] = useState([]);
  const [deletedThreats, setDeletedThreats] = useState([]);
  const [inherentRisks, setInherentRisks] = useState({});
  const [residualRisks, setResidualRisks] = useState({});
  const { locale, t, changeLanguage } = useLocalization();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const toast = useToast();
  
  // Hook para el generador de reportes
  const reportGenerator = ReportGenerator();
  
  // Hook para colores según el modo de color
  const controlBg = useColorModeValue('gray.50', 'gray.700');
  
  // Función para obtener el label del riesgo según OWASP (dentro del componente para acceder a t)
  const getRiskLabel = (riskValue) => {
    const value = parseFloat(riskValue);
    if (value < 3) return t?.ui?.risk_low || "BAJO";
    if (value < 6) return t?.ui?.risk_medium || "MEDIO"; 
    return t?.ui?.risk_high || "ALTO";
  };

  // Función para renderizar los tipos como badges separados
  const renderTypeBadges = (typeString) => {
    if (!typeString) return null;
    
    const types = typeString.split(',').map(type => type.trim()).filter(type => type.length > 0);
    
    return (
      <HStack spacing={1} wrap="wrap">
        {types.map((type, index) => (
          <Badge key={index} colorScheme="blue" size="sm">
            {type}
          </Badge>
        ))}
      </HStack>
    );
  };
  
  // Estados para controlar la vista de la tabla
  const [viewMode, setViewMode] = useState('compact'); // 'compact', 'detailed', 'tabs'
  const [showRiskAssessment, setShowRiskAssessment] = useState(true); // Controla visibilidad de evaluación OWASP
  const [expandedSections, setExpandedSections] = useState({
    'threat_agent': true,
    'vulnerability': false,
    'technical': false,
    'business': false
  });

  // Función helper para obtener colores de riesgo (mejorada)
  const getRiskColor = (risk) => {
    const numericRisk = typeof risk === 'string' ? parseFloat(risk) : risk;
    // Usar los mismos umbrales que getRiskLabel para consistencia
    if (numericRisk >= 6) return 'red.500';
    if (numericRisk >= 3) return 'orange.500';
    return 'green.500';
  };
  
  // Función helper para obtener el colorScheme de Chakra UI
  const getRiskColorScheme = (risk) => {
    const numericRisk = typeof risk === 'string' ? parseFloat(risk) : risk;
    if (numericRisk >= 6) return 'red';
    if (numericRisk >= 3) return 'orange';
    return 'green';
  };
  
  // Función helper para obtener el color CSS del riesgo
  const getRiskColorCSS = (risk) => {
    const numericRisk = typeof risk === 'string' ? parseFloat(risk) : risk;
    if (numericRisk >= 6) return '#e53e3e'; // red.500
    if (numericRisk >= 3) return '#dd6b20'; // orange.500
    return '#38a169'; // green.500
  };

  // Función helper para obtener el valor numérico del riesgo inherente
  const getRiskValue = (threatId) => {
    const risk = inherentRisks[threatId];
    if (risk === undefined || risk === null) return 0;
    return typeof risk === 'number' ? risk : parseFloat(risk) || 0;
  };
  
  // Función helper para obtener el valor numérico del riesgo residual
  const getResidualRiskValue = (threatId) => {
    const risk = residualRisks[threatId];
    if (risk === undefined || risk === null) return 1;
    return typeof risk === 'number' ? risk : parseFloat(risk) || 1;
  };
  
  // Función helper para obtener el riesgo actual (inherente si no hay remediación aplicada, residual si hay)
  const getCurrentRiskValue = (threatId) => {
    const threat = threats.find(t => t.id === threatId);
    const isRemediationApplied = threat?.remediation?.status === true;
    
    console.log(`getCurrentRiskValue para threat ${threatId}:`, {
      threatFound: !!threat,
      remediationStatus: threat?.remediation?.status,
      isRemediationApplied
    });
    
    if (isRemediationApplied) {
      // Si la remediación está aplicada, usar el riesgo residual
      const residualRisk = getResidualRiskValue(threatId);
      console.log(`Usando riesgo residual: ${residualRisk}`);
      return residualRisk;
    } else {
      // Si la remediación no está aplicada, usar el riesgo inherente
      const inherentRisk = getRiskValue(threatId);
      console.log(`Usando riesgo inherente: ${inherentRisk}`);
      return inherentRisk;
    }
  };
  
  // Función para actualizar manualmente el riesgo residual desde un select
  const updateResidualRisk = (threatId, value) => {
    const numericValue = parseFloat(value);
    setResidualRisks(prev => ({
      ...prev,
      [threatId]: numericValue
    }));
  };
  
  // Función helper para crear un switch de remediación
  const createRemediationSwitch = (threat, size = "md") => {
    return (
      <Tooltip
        label={threat.remediation?.status ? 
          (t?.ui?.click_to_mark_not_applied || 'Click to mark as not remediated') : 
          (t?.ui?.click_to_mark_applied || 'Click to mark as remediated')
        }
        placement="top"
        hasArrow
        bg={threat.remediation?.status ? 'red.500' : 'green.500'}
        color="white"
        fontSize="sm"
      >
        <FormControl display="flex" alignItems="center" width="auto">
          <Switch
            id={`remediation-switch-${threat.id}`}
            size={size}
            colorScheme="green"
            isChecked={threat.remediation?.status || false}
            onChange={(e) => {
              const newStatus = e.target.checked;
              updateRemediationStatus(threat.id, newStatus);
            }}
            _focus={{
              boxShadow: "0 0 0 3px rgba(66, 153, 225, 0.6)"
            }}
          />
          <FormLabel 
            htmlFor={`remediation-switch-${threat.id}`} 
            ml={2} 
            mb={0}
            fontSize={size === "sm" ? "xs" : "sm"}
            fontWeight="bold"
            color={threat.remediation?.status ? "green.600" : "red.600"}
            cursor="pointer"
          >
            {threat.remediation?.status ? 
              (t?.ui?.applied || 'Applied') : 
              (t?.ui?.not_applied || 'Not Applied')
            }
          </FormLabel>
        </FormControl>
      </Tooltip>
    );
  };
  
  // Función helper para crear un selector de riesgo residual con apariencia mejorada
  // Estilos centralizados para los componentes de riesgo
  const riskDisplayStyles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '2px',
      width: '100%'
    },
    containerWithSelector: {
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '2px',
      width: '100%',
      cursor: 'pointer'
    },
    numberValue: {
      fontWeight: 'bold',
      fontSize: '16px',
      textAlign: 'center'
    },
    riskLabel: {
      fontSize: '10px',
      fontWeight: 'bold',
      color: 'white',
      padding: '2px 6px',
      borderRadius: '8px',
      textAlign: 'center',
      minWidth: '50px'
    },
    invisibleSelect: {
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      opacity: 0,
      cursor: 'pointer',
      zIndex: 10
    },
    dropdownIcon: {
      position: 'absolute',
      top: '2px',
      right: '2px',
      fontSize: '8px',
      pointerEvents: 'none',
      zIndex: 5
    }
  };

  const createResidualRiskSelector = (threatId, currentValue) => {
    // Crear opciones más granulares (de 1 a 9 con incrementos de 0.5)
    const options = [];
    for (let i = 1; i <= 9; i += 0.5) {
      options.push(i);
    }
    
    const roundedValue = Math.round(currentValue * 2) / 2; // Redondea a múltiplos de 0.5
    const riskColor = getRiskColorCSS(roundedValue);
    const riskLabel = getRiskLabel(roundedValue);
    
    return (
      <div style={riskDisplayStyles.containerWithSelector}>
        {/* Valor numérico grande */}
        <div style={{
          ...riskDisplayStyles.numberValue,
          color: riskColor
        }}>
          {roundedValue.toFixed(1)}
        </div>
        
        {/* Label con color de fondo */}
        <div style={{
          ...riskDisplayStyles.riskLabel,
          backgroundColor: riskColor
        }}>
          {riskLabel}
        </div>
        
        {/* Select invisible superpuesto */}
        <select 
          value={roundedValue}
          onChange={(e) => updateResidualRisk(threatId, e.target.value)}
          style={riskDisplayStyles.invisibleSelect}
        >
          {options.map(value => (
            <option 
              key={value} 
              value={value}
            >
              {value.toFixed(1)} - {getRiskLabel(value)}
            </option>
          ))}
        </select>
        
        {/* Icono de dropdown */}
        <div style={{
          ...riskDisplayStyles.dropdownIcon,
          color: riskColor
        }}>
          ▼
        </div>
      </div>
    );
  };

  // Función para mostrar riesgo inherente con el mismo diseño que residual pero sin edición
  const createInherentRiskDisplay = (riskValue) => {
    const roundedValue = Math.round(riskValue * 2) / 2; // Redondea a múltiplos de 0.5
    const riskColor = getRiskColorCSS(roundedValue);
    const riskLabel = getRiskLabel(roundedValue);
    
    return (
      <div style={riskDisplayStyles.container}>
        {/* Valor numérico grande */}
        <div style={{
          ...riskDisplayStyles.numberValue,
          color: riskColor
        }}>
          {roundedValue.toFixed(1)}
        </div>
        
        {/* Label con color de fondo */}
        <div style={{
          ...riskDisplayStyles.riskLabel,
          backgroundColor: riskColor
        }}>
          {riskLabel}
        </div>
      </div>
    );
  };

  // Función para mostrar riesgo actual con el mismo diseño que residual pero sin edición
  const createCurrentRiskDisplay = (riskValue) => {
    const roundedValue = Math.round(riskValue * 2) / 2; // Redondea a múltiplos de 0.5
    const riskColor = getRiskColorCSS(roundedValue);
    const riskLabel = getRiskLabel(roundedValue);
    
    return (
      <div style={riskDisplayStyles.container}>
        {/* Valor numérico grande */}
        <div style={{
          ...riskDisplayStyles.numberValue,
          color: riskColor
        }}>
          {roundedValue.toFixed(1)}
        </div>
        
        {/* Label con color de fondo */}
        <div style={{
          ...riskDisplayStyles.riskLabel,
          backgroundColor: riskColor
        }}>
          {riskLabel}
        </div>
      </div>
    );
  };

  // Función helper para crear selectores OWASP optimizados
  const createOwaspSelector = (threat, fieldName, labelKey) => {
    const options = getOwaspSelectOptions(fieldName, locale);
    return (
      <VStack align="start" spacing={2}>
        <Text fontSize="sm" fontWeight="bold">
          {t?.owasp?.factors?.[labelKey] || labelKey}
        </Text>
        <select
          value={threat.risk?.[fieldName] || 0}
          style={{ width: "100%", padding: "4px", fontSize: "12px" }}
          onChange={(e) => updateThreatRisk(threat.id, fieldName, parseInt(e.target.value))}
        >
          {options.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </VStack>
    );
  };

  // Función para alternar secciones
  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // Función helper para mostrar notificaciones
  const showNotification = (title, description, status = 'info') => {
    toast({
      title,
      description,
      status, // 'success', 'error', 'warning', 'info'
      duration: status === 'error' ? 6000 : 4000, // Más tiempo para errores
      isClosable: true,
      position: 'top-right',
      variant: 'left-accent', // Estilo más elegante
      containerStyle: {
        maxWidth: '400px'
      }
    });
  };
  
  // Función para actualizar un campo específico de riesgo de amenaza
  const updateThreatRisk = (threatId, fieldName, value) => {
    // Actualizar el campo en la amenaza
    setThreats(prevThreats => 
      prevThreats.map(threat => {
        if (threat.id === threatId) {
          const updatedRisk = { ...threat.risk, [fieldName]: value };
          const updatedThreat = { ...threat, risk: updatedRisk };
          
          // Recalcular el riesgo inherente
          const newInherentRisk = calculateInherentRisk(updatedRisk);
          setInherentRisks(prev => ({
            ...prev,
            [threatId]: newInherentRisk
          }));
          
          return updatedThreat;
        }
        return threat;
      })
    );
    
    // También actualizar en serviceData
    setServiceData(prevData => ({
      ...prevData,
      threats: prevData.threats.map(threat => {
        if (threat.id === threatId) {
          return { ...threat, risk: { ...threat.risk, [fieldName]: value } };
        }
        return threat;
      })
    }));
  };
  
  const fetchData = async () => {
    setIsLoading(true);
    const data = await fetchInformationSystemById(id);
    console.log('=== FETCHDATA DEBUG ===');
    console.log('Fetched data:', data);
    console.log('Data threats:', data?.threats);
    console.log('Number of threats:', data?.threats?.length || 0);
    
    setServiceData(data);
    setThreats(data?.threats || []);
    
    // Inicializar los riesgos inherentes y residuales
    if (data && data.threats) {
      const initialInherentRisks = {};
      const initialResidualRisks = {};
      data.threats.forEach(threat => {
        console.log(`Processing threat ${threat.id}, risk.residual_risk:`, threat.risk?.residual_risk);
        
        const inherentRiskValue = calculateInherentRisk(threat.risk);
        initialInherentRisks[threat.id] = inherentRiskValue;
        
        // Usar el valor guardado del backend si existe, sino usar riesgo inherente como inicial
        let residualRiskValue;
        if (threat.risk && threat.risk.residual_risk !== null && threat.risk.residual_risk !== undefined) {
          // Usar el valor guardado del backend
          residualRiskValue = threat.risk.residual_risk;
        } else {
          // Si no hay valor guardado, usar el riesgo inherente como valor inicial
          residualRiskValue = inherentRiskValue;
        }
        
        initialResidualRisks[threat.id] = residualRiskValue;
      });
      setInherentRisks(initialInherentRisks);
      setResidualRisks(initialResidualRisks);
    }
    
    setIsLoading(false);
  };
  
  // Función para actualizar el riesgo inherente cuando cambian los valores OWASP
  const updateInherentRisk = async (threatId) => {
    // Threat Agent Factors
    const skill_level = Number(document.getElementById(`skill_level-${threatId}`)?.value || 0);
    const motive = Number(document.getElementById(`motive-${threatId}`)?.value || 0);
    const opportunity = Number(document.getElementById(`opportunity-${threatId}`)?.value || 0);
    const size = Number(document.getElementById(`size-${threatId}`)?.value || 0);
    
    // Vulnerability Factors
    const ease_of_discovery = Number(document.getElementById(`ease_of_discovery-${threatId}`)?.value || 0);
    const ease_of_exploit = Number(document.getElementById(`ease_of_exploit-${threatId}`)?.value || 0);
    const awareness = Number(document.getElementById(`awareness-${threatId}`)?.value || 0);
    const intrusion_detection = Number(document.getElementById(`intrusion_detection-${threatId}`)?.value || 0);
    
    // Technical Impact
    const loss_of_confidentiality = Number(document.getElementById(`loss_of_confidentiality-${threatId}`)?.value || 0);
    const loss_of_integrity = Number(document.getElementById(`loss_of_integrity-${threatId}`)?.value || 0);
    const loss_of_availability = Number(document.getElementById(`loss_of_availability-${threatId}`)?.value || 0);
    const loss_of_accountability = Number(document.getElementById(`loss_of_accountability-${threatId}`)?.value || 0);
    
    // Business Impact
    const financial_damage = Number(document.getElementById(`financial_damage-${threatId}`)?.value || 0);
    const reputation_damage = Number(document.getElementById(`reputation_damage-${threatId}`)?.value || 0);
    const non_compliance = Number(document.getElementById(`non_compliance-${threatId}`)?.value || 0);
    const privacy_violation = Number(document.getElementById(`privacy_violation-${threatId}`)?.value || 0);
    
    const likelihoodFactors = [skill_level, motive, opportunity, size, ease_of_discovery, ease_of_exploit, awareness, intrusion_detection];
    const impactFactors = [loss_of_confidentiality, loss_of_integrity, loss_of_availability, loss_of_accountability, financial_damage, reputation_damage, non_compliance, privacy_violation];
    
    const likelihood = likelihoodFactors.reduce((acc, val) => acc + val, 0) / likelihoodFactors.length;
    const impact = impactFactors.reduce((acc, val) => acc + val, 0) / impactFactors.length;
    const overallRisk = (likelihood + impact) / 2;
    
    setInherentRisks(prev => ({
      ...prev,
      [threatId]: overallRisk
    }));
    
    // Encontrar el threat para obtener el estado de remediación
    const currentThreat = threats.find(threat => threat.id === threatId);
    if (currentThreat) {
      // No actualizar automáticamente el riesgo residual, mantener el valor manual del usuario
      // El riesgo residual ahora se maneja completamente de forma manual
    }

    // Actualizar el riesgo en el backend
    const riskData = {
      skill_level,
      motive,
      opportunity,
      size,
      ease_of_discovery,
      ease_of_exploit,
      awareness,
      intrusion_detection,
      loss_of_confidentiality,
      loss_of_integrity,
      loss_of_availability,
      loss_of_accountability,
      financial_damage,
      reputation_damage,
      non_compliance,
      privacy_violation
    };

    try {
      await fetch(`http://localhost:8000/threat/${threatId}/risk`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(riskData),
      });

      // Actualizar el estado local de las amenazas
      setThreats(prevThreats => 
        prevThreats.map(threat => 
          threat.id === threatId 
            ? { 
                ...threat, 
                risk: { ...threat.risk, ...riskData } 
              }
            : threat
        )
      );
    } catch (error) {
      console.error('Error updating risk:', error);
    }
  };
  
  // Función para actualizar el estado de la remediación
  const updateRemediationStatus = (threatId, status) => {
    console.log(`Actualizando remediación para threat ${threatId}: ${status ? 'aplicada' : 'removida'}`);
    
    // Actualizar el estado local de threats
    setThreats(prevThreats => 
      prevThreats.map(threat => 
        threat.id === threatId 
          ? { 
              ...threat, 
              remediation: { ...threat.remediation, status } 
            }
          : threat
      )
    );
    
    // También actualizar el estado de serviceData para mantener consistencia
    setServiceData(prevData => ({
      ...prevData,
      threats: prevData.threats.map(threat => 
        threat.id === threatId 
          ? { 
              ...threat, 
              remediation: { ...threat.remediation, status } 
            }
          : threat
      )
    }));
    
    // El riesgo residual ahora se maneja completamente de forma manual
    // No se actualiza automáticamente cuando cambia el estado de remediación
    console.log(`Remediación ${status ? 'aplicada' : 'removida'} para threat ${threatId}. Riesgo residual se mantiene manual.`);
    
    // Forzar re-render al actualizar el estado (esto debería triggerear getCurrentRiskValue)
    console.log('Estados actualizados, debería re-renderizar getCurrentRiskValue');
  };
  
  // Función para generar informe PDF (usando el componente ReportGenerator)
  const generateReport = async () => {
    await reportGenerator.generateReport(
      serviceData,
      threats,
      getRiskValue,
      getResidualRiskValue,
      getCurrentRiskValue,
      calculateInherentRisk,
      getOwaspSelectOptions,
      showNotification
    );
  };
  
  useEffect(() => {
    fetchData();
  }, [id, locale]);
  
  if (isLoading || !serviceData){
    return (
        <div className="App">
          <h1>{t?.ui?.loading || 'Loading...'}</h1>
        </div>
      );
  }
  return (
    <Box
      padding="0.5rem"
      style={{ marginBottom: "160px" }}
    >
      <Card mb={6} shadow="lg" borderRadius="lg" bg="white">
        <CardHeader bg="blue.500" color="white" borderTopRadius="lg">
          <Text fontSize="xl" fontWeight="bold">
            {t?.ui?.system_information || 'System Information'}
          </Text>
        </CardHeader>
        <CardBody>
          <Grid templateColumns="120px 1fr" gap={4} alignItems="start" mb={6}>
            <GridItem>
              <Text fontWeight="bold" color="blue.600" fontSize="md">
                {t?.ui?.title || 'Title'}:
              </Text>
            </GridItem>
            <GridItem>
              <Text fontSize="md" color="gray.700">
                {serviceData.title}
              </Text>
            </GridItem>
            
            <GridItem>
              <Text fontWeight="bold" color="blue.600" fontSize="md">
                {t?.ui?.description || 'Description'}:
              </Text>
            </GridItem>
            <GridItem>
              <Text fontSize="md" color="gray.700" lineHeight="1.5">
                {serviceData.description}
              </Text>
            </GridItem>
          </Grid>
          
          <Box>
            <Text fontWeight="bold" color="blue.600" fontSize="md" mb={4}>
              {t?.ui?.diagram || 'Diagram'}:
            </Text>
            <Flex justifyContent="center">
              <ChakraImage 
                src={`http://localhost:8000/diagrams/${serviceData.diagram}`} 
                alt={serviceData.title}
                maxWidth="600px"
                maxHeight="400px"
                objectFit="contain"
                border="1px solid"
                borderColor="gray.200"
                borderRadius="md"
                shadow="md"
                cursor="pointer"
                _hover={{ shadow: "lg", transform: "scale(1.02)" }}
                transition="all 0.2s"
                onClick={onOpen}
              />
            </Flex>
          </Box>
        </CardBody>
      </Card>
      
      <Text fontSize="xl" fontWeight="bold" color="blue.600" mb={4}>
        {t?.ui?.threats || 'Threats'}:
      </Text>
      
      {/* Controles de vista */}
      <HStack spacing={4} mb={4} p={4} bg={controlBg} borderRadius="md" flexWrap="wrap">
        <HStack spacing={4}>
          <Text fontWeight="bold">{t?.ui?.view_mode || 'View Mode'}:</Text>
          <Button
            size="sm"
            leftIcon={<FaThLarge />}
            variant={viewMode === 'compact' ? 'solid' : 'outline'}
            colorScheme="blue"
            onClick={() => setViewMode('compact')}
          >
            {t?.ui?.compact || 'Compact'}
          </Button>
          <Button
            size="sm"
            leftIcon={<FaTable />}
            variant={viewMode === 'detailed' ? 'solid' : 'outline'}
            colorScheme="blue"
            onClick={() => setViewMode('detailed')}
          >
            {t?.ui?.detailed || 'Detailed'}
          </Button>
          <Button
            size="sm"
            leftIcon={<FaEdit />}
            variant={viewMode === 'tabs' ? 'solid' : 'outline'}
            colorScheme="blue"
            onClick={() => setViewMode('tabs')}
          >
            {t?.ui?.tabs || 'Tabs'}
          </Button>
        </HStack>
        
        {/* Toggle para ocultar/mostrar evaluación del riesgo (solo en vista detallada) */}
        {viewMode === 'detailed' && (
          <HStack spacing={2} ml={4}>
            <Divider orientation="vertical" height="30px" />
            <Tooltip 
              label={showRiskAssessment ? 
                (t?.ui?.hide_owasp_calculator || "Ocultar calculadora OWASP Risk Rating") : 
                (t?.ui?.show_owasp_calculator || "Mostrar calculadora OWASP Risk Rating")
              }
              placement="top"
            >
              <Button
                size="sm"
                leftIcon={showRiskAssessment ? <FaEyeSlash /> : <FaEye />}
                variant="outline"
                colorScheme={showRiskAssessment ? "orange" : "green"}
                onClick={() => setShowRiskAssessment(!showRiskAssessment)}
              >
                {showRiskAssessment ? 
                  (t?.ui?.hide_owasp_rating || "Ocultar OWASP Risk Rating") : 
                  (t?.ui?.show_owasp_rating || "Mostrar OWASP Risk Rating")
                }
              </Button>
            </Tooltip>
          </HStack>
        )}
      </HStack>

      {viewMode === 'compact' && (
        <Card mb={4}>
          <CardBody>
            <VStack spacing={4}>
              {threats.map((threat, index) => (
                <Card key={threat.id} w="100%" variant="outline">
                  <CardBody>
                    <HStack justify="space-between" align="start">
                      <VStack align="start" flex="1">
                        <HStack>
                          {renderTypeBadges(threat.type)}
                          <Text fontWeight="bold" fontSize="lg">{threat.title}</Text>
                        </HStack>
                        <Text color="gray.600" fontSize="sm" noOfLines={2}>
                          {threat.description}
                        </Text>
                        <VStack spacing={2} align="stretch">
                          <HStack justify="space-between" align="center" wrap="wrap">
                            <HStack minW="150px">
                              <Text fontSize="sm" minW="60px">
                                <strong>{t?.ui?.inherent_risk || 'IR'}:</strong>
                              </Text>
                              <Badge colorScheme={getRiskColorScheme(getRiskValue(threat.id))} fontSize="sm">
                                {getRiskValue(threat.id).toFixed(1)}
                              </Badge>
                            </HStack>
                            
                            <HStack minW="150px">
                              <Text fontSize="sm" minW="60px">
                                <strong>{t?.ui?.residual_risk || 'RR'}:</strong>
                              </Text>
                              <Badge colorScheme={getRiskColorScheme(getResidualRiskValue(threat.id))} fontSize="sm">
                                {getResidualRiskValue(threat.id).toFixed(1)}
                              </Badge>
                            </HStack>
                            
                            <HStack minW="150px">
                              <Text fontSize="sm" minW="60px">
                                <strong>{t?.ui?.current_risk || 'CR'}:</strong>
                              </Text>
                              <Badge colorScheme={getRiskColorScheme(getCurrentRiskValue(threat.id))} fontSize="sm">
                                {getCurrentRiskValue(threat.id).toFixed(1)}
                              </Badge>
                            </HStack>
                          </HStack>
                          
                          <HStack justify="center" align="center">
                            <Text fontSize="sm">
                              <strong>{t?.ui?.remediation || 'Remediation'}:</strong>
                            </Text>
                            {createRemediationSwitch(threat, "sm")}
                          </HStack>
                        </VStack>
                      </VStack>
                      <VStack>
                        <Button
                          size="sm"
                          colorScheme="blue"
                          variant="outline"
                          leftIcon={<FaEdit />}
                          onClick={() => setViewMode('detailed')}
                        >
                          {t?.ui?.edit || 'Edit'}
                        </Button>
                        <Button
                          size="sm"
                          colorScheme="red"
                          variant="outline"
                          leftIcon={<FaTrash />}
                          onClick={() => {
                            const threatTitle = threat.title || 'Amenaza';
                            
                            setDeletedThreats(prev => prev.includes(threat.id) ? prev : [...prev, threat.id]);
                            
                            setServiceData(prev => {
                              const newThreats = prev.threats.filter(t => t.id !== threat.id);
                              return { ...prev, threats: newThreats };
                            });
                            
                            setThreats(prev => prev.filter(t => t.id !== threat.id));
                            
                            setInherentRisks(prev => {
                              const updated = { ...prev };
                              delete updated[threat.id];
                              return updated;
                            });
                            
                            showNotification(
                              t?.ui?.threat_deleted_title || "Threat Marked for Deletion",
                              t?.ui?.threat_deleted || `"${threatTitle}" will be deleted when you save changes`,
                              'info'
                            );
                          }}
                        >
                          {t?.ui?.delete || 'Delete'}
                        </Button>
                      </VStack>
                    </HStack>
                  </CardBody>
                </Card>
              ))}
            </VStack>
          </CardBody>
        </Card>
      )}

      {viewMode === 'tabs' && (
        <Tabs variant="enclosed" colorScheme="blue">
          <TabList>
            {threats.map((threat, index) => (
              <Tab key={threat.id} maxWidth="200px" overflow="hidden" textOverflow="ellipsis">
                <VStack spacing={1}>
                  <Text fontSize="sm" fontWeight="bold" noOfLines={1}>
                    {threat.title}
                  </Text>
                  <HStack spacing={1}>
                    <Badge colorScheme={getRiskColorScheme(getRiskValue(threat.id))} fontSize="xs">
                      IR: {getRiskValue(threat.id).toFixed(1)}
                    </Badge>
                    <Badge colorScheme={getRiskColorScheme(getResidualRiskValue(threat.id))} fontSize="xs">
                      RR: {getResidualRiskValue(threat.id).toFixed(1)}
                    </Badge>
                    <Badge colorScheme={getRiskColorScheme(getCurrentRiskValue(threat.id))} fontSize="xs">
                      CR: {getCurrentRiskValue(threat.id).toFixed(1)}
                    </Badge>
                  </HStack>
                </VStack>
              </Tab>
            ))}
          </TabList>
          <TabPanels>
            {threats.map((threat) => (
              <TabPanel key={threat.id}>
                <Card>
                  <CardBody>
                    <VStack spacing={4} align="stretch">
                      <HStack justify="space-between">
                        <VStack align="start">
                          <Text fontWeight="bold" fontSize="xl">{threat.title}</Text>
                          {renderTypeBadges(threat.type)}
                        </VStack>
                        <Button
                          colorScheme="red"
                          variant="outline"
                          size="sm"
                          leftIcon={<FaTrash />}
                          onClick={() => {
                            const threatTitle = threat.title || 'Amenaza';
                            setDeletedThreats(prev => prev.includes(threat.id) ? prev : [...prev, threat.id]);
                            setServiceData(prev => ({
                              ...prev,
                              threats: prev.threats.filter(t => t.id !== threat.id)
                            }));
                            setThreats(prev => prev.filter(t => t.id !== threat.id));
                            setInherentRisks(prev => {
                              const updated = { ...prev };
                              delete updated[threat.id];
                              return updated;
                            });
                            showNotification(
                              t?.ui?.threat_deleted_title || "Threat Marked for Deletion",
                              t?.ui?.threat_deleted || `"${threatTitle}" will be deleted when you save changes`,
                              'info'
                            );
                          }}
                        >
                          {t?.ui?.delete || 'Delete'}
                        </Button>
                      </HStack>
                      
                      <Text color="gray.600">{threat.description}</Text>
                      
                      <Accordion allowMultiple defaultIndex={[0]}>
                        <AccordionItem>
                          <AccordionButton>
                            <Box flex="1" textAlign="left" fontWeight="bold">
                              {t?.owasp?.categories?.threat_agent_factors || 'Threat Agent Factors'}
                            </Box>
                            <AccordionIcon />
                          </AccordionButton>
                          <AccordionPanel>
                            <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                              {createOwaspSelector(threat, 'skill_level', 'skill_level')}
                              {createOwaspSelector(threat, 'motive', 'motive')}
                              {createOwaspSelector(threat, 'opportunity', 'opportunity')}
                              {createOwaspSelector(threat, 'size', 'size')}
                            </Grid>
                          </AccordionPanel>
                        </AccordionItem>
                        
                        <AccordionItem>
                          <AccordionButton>
                            <Box flex="1" textAlign="left" fontWeight="bold">
                              {t?.owasp?.categories?.vulnerability_factors || 'Vulnerability Factors'}
                            </Box>
                            <AccordionIcon />
                          </AccordionButton>
                          <AccordionPanel>
                            <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                              {createOwaspSelector(threat, 'ease_of_discovery', 'ease_of_discovery')}
                              {createOwaspSelector(threat, 'ease_of_exploit', 'ease_of_exploit')}
                              {createOwaspSelector(threat, 'awareness', 'awareness')}
                              {createOwaspSelector(threat, 'intrusion_detection', 'intrusion_detection')}
                            </Grid>
                          </AccordionPanel>
                        </AccordionItem>
                        
                        <AccordionItem>
                          <AccordionButton>
                            <Box flex="1" textAlign="left" fontWeight="bold">
                              {t?.owasp?.categories?.technical_impact || 'Technical Impact'}
                            </Box>
                            <AccordionIcon />
                          </AccordionButton>
                          <AccordionPanel>
                            <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                              {createOwaspSelector(threat, 'loss_of_confidentiality', 'loss_of_confidentiality')}
                              {createOwaspSelector(threat, 'loss_of_integrity', 'loss_of_integrity')}
                              {createOwaspSelector(threat, 'loss_of_availability', 'loss_of_availability')}
                              {createOwaspSelector(threat, 'loss_of_accountability', 'loss_of_accountability')}
                            </Grid>
                          </AccordionPanel>
                        </AccordionItem>
                        
                        <AccordionItem>
                          <AccordionButton>
                            <Box flex="1" textAlign="left" fontWeight="bold">
                              {t?.owasp?.categories?.business_impact || 'Business Impact'}
                            </Box>
                            <AccordionIcon />
                          </AccordionButton>
                          <AccordionPanel>
                            <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                              {createOwaspSelector(threat, 'financial_damage', 'financial_damage')}
                              {createOwaspSelector(threat, 'reputation_damage', 'reputation_damage')}
                              {createOwaspSelector(threat, 'non_compliance', 'non_compliance')}
                              {createOwaspSelector(threat, 'privacy_violation', 'privacy_violation')}
                            </Grid>
                          </AccordionPanel>
                        </AccordionItem>
                        
                      </Accordion>
                      
                      <VStack align="stretch" spacing={3}>
                        <HStack justify="space-between" align="center">
                          <Text fontWeight="bold" fontSize="md">{t?.ui?.remediation || 'Remediation'}:</Text>
                          {createRemediationSwitch(threat, "md")}
                        </HStack>
                        
                        <Text fontSize="sm" color="gray.600" fontStyle="italic">
                          {threat.remediation?.description || 'No remediation description available'}
                        </Text>
                      </VStack>
                      
                      <HStack spacing={6} align="flex-start">
                        <VStack align="flex-start" spacing={1}>
                          <Text fontWeight="bold">{t?.ui?.inherent_risk || 'Inherent Risk'}:</Text>
                          <Box width="100px">
                            {createInherentRiskDisplay(getRiskValue(threat.id))}
                          </Box>
                        </VStack>
                        <VStack align="flex-start" spacing={1}>
                          <Text fontWeight="bold">{t?.ui?.residual_risk || 'Residual Risk'}:</Text>
                          <Box width="100px">
                            {createResidualRiskSelector(threat.id, getResidualRiskValue(threat.id))}
                          </Box>
                        </VStack>
                        <VStack align="flex-start" spacing={1}>
                          <Text fontWeight="bold">{t?.ui?.current_risk || 'Current Risk'}:</Text>
                          <Box width="100px">
                            {createCurrentRiskDisplay(getCurrentRiskValue(threat.id))}
                          </Box>
                        </VStack>
                      </HStack>
                    </VStack>
                  </CardBody>
                </Card>
              </TabPanel>
            ))}
          </TabPanels>
        </Tabs>
      )}

      {viewMode === 'detailed' && (
      <TableContainer key={locale}>
        <Table border="2px solid gray" borderCollapse="collapse" overflowX='auto' whiteSpace='normal'>
          <Thead>
            {/* Fila de título principal */}
            <Tr bg="blue.600" color="white" p="2">
              <Th rowSpan="3" p="4" shadow="md" borderRight="2px solid white" bg="blue.600" color="white">{t?.ui?.title || 'Title'}</Th>
              <Th rowSpan="3" p="4" shadow="md" maxWidth='100px' borderRight="2px solid white" bg="blue.600" color="white">{t?.ui?.type || 'Type'}</Th>
              <Th rowSpan="3" p="4" shadow="md" borderRight="2px solid white" bg="blue.600" color="white">{t?.ui?.description || 'Description'}</Th>
              <Th rowSpan="3" p="4" shadow="md" maxWidth='200px' borderRight="2px solid white" bg="blue.600" color="white">{t?.ui?.remediation || 'Remediation'}</Th>
              {showRiskAssessment && (
                <Th colSpan="16" p="2" shadow="md" textAlign="center" borderRight="2px solid white" fontSize="lg" fontWeight="bold" bg="blue.600" color="white">{t?.ui?.owasp_risk_rating || 'OWASP Risk Rating'}</Th>
              )}
              <Th rowSpan="3" p="4" shadow="md" maxWidth='100px' borderRight="2px solid white" bg="blue.600" color="white">{t?.ui?.inherent_risk || 'Inherent Risk'}</Th>
              <Th rowSpan="3" p="4" shadow="md" maxWidth='100px' borderRight="2px solid white" bg="blue.600" color="white">{t?.ui?.residual_risk || 'Residual Risk'}</Th>
              <Th rowSpan="3" p="4" shadow="md" maxWidth='100px' borderRight="2px solid white" bg="blue.600" color="white">{t?.ui?.current_risk || 'Current Risk'}</Th>
              <Th rowSpan="3" p="4" shadow="md" maxWidth='100px' borderRight="2px solid white" bg="blue.600" color="white">{t?.ui?.applied || 'Remediada'}</Th>
              <Th rowSpan="3" p="4" shadow="md" maxWidth='100px' bg="blue.600" color="white">{t?.ui?.delete || 'Delete'}</Th>
            </Tr>
            {/* Fila de categorías padre */}
            <Tr bg="blue.400" color="white" p="2">
              {showRiskAssessment && (
                <>
                  <Th colSpan="4" p="2" shadow="md" textAlign="center" borderRight="2px solid #4299e1" fontSize="sm" bg="blue.100" color="blue.800">{t.owasp.categories.threat_agent_factors}</Th>
                  <Th colSpan="4" p="2" shadow="md" textAlign="center" borderRight="2px solid #ed8936" fontSize="sm" bg="orange.100" color="orange.800">{t.owasp.categories.vulnerability_factors}</Th>
                  <Th colSpan="4" p="2" shadow="md" textAlign="center" borderRight="2px solid #e53e3e" fontSize="sm" bg="red.100" color="red.800">{t.owasp.categories.technical_impact}</Th>
                  <Th colSpan="4" p="2" shadow="md" textAlign="center" borderRight="2px solid #805ad5" fontSize="sm" bg="purple.100" color="purple.800">{t.owasp.categories.business_impact}</Th>
                </>
              )}
            </Tr>
            {/* Fila de parámetros específicos */}
            <Tr bg="gray.300" color="white" p="4" fontSize="xs">
              {showRiskAssessment && (
                <>
                  <Th p="2" shadow="md" maxWidth='120px' fontSize="xs" bg="blue.100" color="blue.800" borderRight="1px solid #4299e1">{t.owasp.factors.skill_level}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' fontSize="xs" bg="blue.100" color="blue.800" borderRight="1px solid #4299e1">{t.owasp.factors.motive}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' fontSize="xs" bg="blue.100" color="blue.800" borderRight="1px solid #4299e1">{t.owasp.factors.opportunity}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' borderRight="2px solid #4299e1" fontSize="xs" bg="blue.100" color="blue.800">{t.owasp.factors.size}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' fontSize="xs" bg="orange.100" color="orange.800" borderRight="1px solid #ed8936">{t.owasp.factors.ease_of_discovery}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' fontSize="xs" bg="orange.100" color="orange.800" borderRight="1px solid #ed8936">{t.owasp.factors.ease_of_exploit}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' fontSize="xs" bg="orange.100" color="orange.800" borderRight="1px solid #ed8936">{t.owasp.factors.awareness}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' borderRight="2px solid #ed8936" fontSize="xs" bg="orange.100" color="orange.800">{t.owasp.factors.intrusion_detection}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' fontSize="xs" bg="red.100" color="red.800" borderRight="1px solid #e53e3e">{t.owasp.factors.loss_of_confidentiality}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' fontSize="xs" bg="red.100" color="red.800" borderRight="1px solid #e53e3e">{t.owasp.factors.loss_of_integrity}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' fontSize="xs" bg="red.100" color="red.800" borderRight="1px solid #e53e3e">{t.owasp.factors.loss_of_availability}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' borderRight="2px solid #e53e3e" fontSize="xs" bg="red.100" color="red.800">{t.owasp.factors.loss_of_accountability}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' fontSize="xs" bg="purple.100" color="purple.800" borderRight="1px solid #805ad5">{t.owasp.factors.financial_damage}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' fontSize="xs" bg="purple.100" color="purple.800" borderRight="1px solid #805ad5">{t.owasp.factors.reputation_damage}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' fontSize="xs" bg="purple.100" color="purple.800" borderRight="1px solid #805ad5">{t.owasp.factors.non_compliance}</Th>
                  <Th p="2" shadow="md" maxWidth='120px' borderRight="2px solid #805ad5" fontSize="xs" bg="purple.100" color="purple.800">{t.owasp.factors.privacy_violation}</Th>
                </>
              )}
            </Tr>
          </Thead>
          <Tbody>
            {threats.map((threat) => (
              <Tr key={threat.id}>
                
                <Td p="4" shadow="md" maxWidth="200px">
                  <textarea 
                    defaultValue={threat.title} 
                    style={{
                      width: "120px", 
                      height: `${calculateTextareaHeight(threat.title, 120)}px`,
                      resize: "vertical",
                      overflow: "hidden",
                      fontFamily: "inherit",
                      fontSize: "14px"
                    }} 
                    id={`title-${threat.id}`}
                    onInput={handleTextareaResize}
                  />
                </Td>
                <Td p="4" shadow="md" maxWidth="100px">
                  <textarea 
                    defaultValue={threat.type} 
                    style={{
                      width: "80px", 
                      height: `${calculateTextareaHeight(threat.type, 80)}px`,
                      resize: "vertical",
                      overflow: "hidden",
                      fontFamily: "inherit",
                      fontSize: "14px"
                    }} 
                    id={`type-${threat.id}`}
                    onInput={handleTextareaResize}
                  />
                </Td>
                <Td p="4" shadow="md" style={{ whiteSpace: "normal", maxWidth: "200px", overflowWrap: "break-word" }}>
                  <textarea 
                    defaultValue={threat.description} 
                    style={{
                      width: "180px", 
                      height: `${calculateTextareaHeight(threat.description, 180)}px`,
                      resize: "vertical",
                      overflow: "hidden",
                      fontFamily: "inherit",
                      fontSize: "14px"
                    }} 
                    id={`description-${threat.id}`}
                    onInput={handleTextareaResize}
                  />
                </Td>
                <Td p="4" shadow="md" style={{ whiteSpace: "normal", maxWidth: "200px", overflowWrap: "break-word" }}>
                  <textarea 
                    defaultValue={threat.remediation.description} 
                    style={{
                      width: "180px", 
                      height: `${calculateTextareaHeight(threat.remediation.description, 180)}px`,
                      resize: "vertical",
                      overflow: "hidden",
                      fontFamily: "inherit",
                      fontSize: "14px"
                    }} 
                    id={`remediation-${threat.id}`}
                    onInput={handleTextareaResize}
                  />
                </Td>
                {/* Columnas OWASP - Solo se muestran si showRiskAssessment es true */}
                {showRiskAssessment && (
                  <>
                    {/* Threat Agent Factors */}
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="blue.50">
                      <OwaspSelector
                        factorName="skill_level"
                        threatId={threat.id}
                        value={threat.risk.skill_level || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="blue.50">
                      <OwaspSelector
                        factorName="motive"
                        threatId={threat.id}
                        value={threat.risk.motive || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="blue.50">
                      <OwaspSelector
                        factorName="opportunity"
                        threatId={threat.id}
                        value={threat.risk.opportunity || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="blue.50" borderRight="2px solid #4299e1">
                      <OwaspSelector
                        factorName="size"
                        threatId={threat.id}
                        value={threat.risk.size || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    
                    {/* Vulnerability Factors */}
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="orange.50">
                      <OwaspSelector
                        factorName="ease_of_discovery"
                        threatId={threat.id}
                        value={threat.risk.ease_of_discovery || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="orange.50">
                      <OwaspSelector
                        factorName="ease_of_exploit"
                        threatId={threat.id}
                        value={threat.risk.ease_of_exploit || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="orange.50">
                      <OwaspSelector
                        factorName="awareness"
                        threatId={threat.id}
                        value={threat.risk.awareness || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="orange.50" borderRight="2px solid #ed8936">
                      <OwaspSelector
                        factorName="intrusion_detection"
                        threatId={threat.id}
                        value={threat.risk.intrusion_detection || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    
                    {/* Technical Impact */}
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="red.50">
                      <OwaspSelector
                        factorName="loss_of_confidentiality"
                        threatId={threat.id}
                        value={threat.risk.loss_of_confidentiality || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="red.50">
                      <OwaspSelector
                        factorName="loss_of_integrity"
                        threatId={threat.id}
                        value={threat.risk.loss_of_integrity || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="red.50">
                      <OwaspSelector
                        factorName="loss_of_availability"
                        threatId={threat.id}
                        value={threat.risk.loss_of_availability || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="red.50" borderRight="2px solid #e53e3e">
                      <OwaspSelector
                        factorName="loss_of_accountability"
                        threatId={threat.id}
                        value={threat.risk.loss_of_accountability || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    
                    {/* Business Impact */}
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="purple.50">
                      <OwaspSelector
                        factorName="financial_damage"
                        threatId={threat.id}
                        value={threat.risk.financial_damage || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="purple.50">
                      <OwaspSelector
                        factorName="reputation_damage"
                        threatId={threat.id}
                        value={threat.risk.reputation_damage || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="purple.50">
                      <OwaspSelector
                        factorName="non_compliance"
                        threatId={threat.id}
                        value={threat.risk.non_compliance || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                    <Td p="4" shadow="md" style={{width: "120px", minWidth: "120px"}} bg="purple.50" borderRight="2px solid #805ad5">
                      <OwaspSelector
                        factorName="privacy_violation"
                        threatId={threat.id}
                        value={threat.risk.privacy_violation || 0}
                        onChange={updateInherentRisk}
                        locale={locale}
                      />
                    </Td>
                  </>
                )}
                
                <Td p="4" shadow="md" style={{width: "80px", minWidth: "80px", textAlign: "center"}}>
                  <div style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    gap: "2px"
                  }}>
                    <span style={{
                      fontWeight: "bold", 
                      color: getRiskColorCSS(getRiskValue(threat.id)), 
                      fontSize: "16px"
                    }}>
                      {getRiskValue(threat.id).toFixed(2)}
                    </span>
                    <span style={{
                      fontSize: "10px",
                      fontWeight: "bold",
                      backgroundColor: getRiskColorCSS(getRiskValue(threat.id)),
                      color: "white",
                      padding: "2px 6px",
                      borderRadius: "8px",
                      textAlign: "center"
                    }}>
                      {getRiskLabel(getRiskValue(threat.id))}
                    </span>
                  </div>
                </Td>
                <Td p="4" shadow="md" style={{width: "100px", minWidth: "100px"}}>
                  {createResidualRiskSelector(threat.id, getResidualRiskValue(threat.id))}
                </Td>
                <Td p="4" shadow="md" style={{width: "100px", minWidth: "100px"}}>
                  <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '2px'
                  }}>
                    <div style={{
                      fontWeight: 'bold',
                      fontSize: '16px',
                      color: getRiskColorCSS(getCurrentRiskValue(threat.id)),
                      textAlign: 'center'
                    }}>
                      {getCurrentRiskValue(threat.id).toFixed(1)}
                    </div>
                    <span style={{
                      fontSize: '10px',
                      fontWeight: 'bold',
                      backgroundColor: getRiskColorCSS(getCurrentRiskValue(threat.id)),
                      color: 'white',
                      padding: '2px 6px',
                      borderRadius: '8px',
                      textAlign: "center"
                    }}>
                      {getRiskLabel(getCurrentRiskValue(threat.id))}
                    </span>
                  </div>
                </Td>
                <Td p="4" shadow="md" style={{width: "100px", minWidth: "100px", textAlign: "center"}}>
                  <FormControl display="flex" alignItems="center" justifyContent="center" flexDirection="column">
                    <Switch
                      size="sm"
                      colorScheme="green"
                      isChecked={threat.remediation?.status || false}
                      onChange={(e) => {
                        const newStatus = e.target.checked;
                        updateRemediationStatus(threat.id, newStatus);
                      }}
                    />
                    <Text fontSize="xs" mt={1} fontWeight="bold" color={threat.remediation?.status ? "green.600" : "red.600"}>
                      {threat.remediation?.status ? (t?.ui?.yes || 'Yes') : (t?.ui?.no || 'No')}
                    </Text>
                  </FormControl>
                </Td>
                <Td p="4" shadow="md">
                  <button
                    type="button"
                    style={{ background: '#e2e8f0', color: '#2d3748', border: 'none', borderRadius: '4px', padding: '4px 10px', cursor: 'pointer' }}
                    aria-label="Eliminar amenaza"
                    title="Eliminar amenaza"
                    onClick={() => {
                      const threatTitle = threat.title || 'Amenaza';
                      
                      setDeletedThreats(prev => prev.includes(threat.id) ? prev : [...prev, threat.id]);
                      
                      // Actualizar ambos estados para eliminar el threat
                      setServiceData(prev => {
                        const newThreats = prev.threats.filter(t => t.id !== threat.id);
                        return { ...prev, threats: newThreats };
                      });
                      
                      // También actualizar el estado threats independiente
                      setThreats(prev => prev.filter(t => t.id !== threat.id));
                      
                      // Eliminar el riesgo inherente del threat eliminado
                      setInherentRisks(prev => {
                        const updated = { ...prev };
                        delete updated[threat.id];
                        return updated;
                      });
                      
                      // Mostrar notificación de eliminación
                      showNotification(
                        t?.ui?.threat_deleted_title || "Threat Marked for Deletion",
                        t?.ui?.threat_deleted || `"${threatTitle}" will be deleted when you save changes`,
                        'info'
                      );
                    }}
                  ><FaTrash size={20} /></button>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </TableContainer>
      )}
      
      <div style={{ display: 'flex', justifyContent: 'center', gap: '15px', marginTop: '20px' }}>
        <button
          type="button"
          style={{ padding: '10px 30px', fontSize: '16px', background: '#38a169', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}
          onClick={generateReport}
        >
          <FaFilePdf size={16} />
          {t?.ui?.generate_report || 'Generate Report'}
        </button>
        <button
          type="button"
          style={{ padding: '10px 30px', fontSize: '16px', background: '#38a169', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
          onClick={async () => {
            try {
              // Crear un nuevo threat en el backend
              const newThreatData = {
                title: "Nueva Amenaza",
                type: "Spoofing",
                description: "Descripción de la nueva amenaza",
                remediation: {
                  description: "Descripción de la remediación",
                  status: false
                },
                risk: {
                  damage: 1,
                  reproducibility: 1,
                  exploitability: 1,
                  affected_users: 1,
                  discoverability: 1,
                  compliance: 1
                }
              };
              
              const response = await createThreatForSystem(id, newThreatData);
              const createdThreat = response.data;
              
              // Agregar el nuevo threat al estado local (ambos estados)
              setServiceData(prev => ({
                ...prev,
                threats: [...prev.threats, createdThreat]
              }));
              
              // También actualizar el estado threats independiente
              setThreats(prev => [...prev, createdThreat]);
              
              // Inicializar el riesgo inherente para el nuevo threat
              setInherentRisks(prev => ({
                ...prev,
                [createdThreat.id]: calculateInherentRisk(createdThreat.risk)
              }));
              
              showNotification(
                t?.ui?.new_threat_success_title || "Success!",
                t?.ui?.new_threat_success || "New threat added successfully",
                'success'
              );
            } catch (error) {
              console.error("Error creando nueva amenaza:", error);
              showNotification(
                t?.ui?.new_threat_error_title || "Error",
                t?.ui?.new_threat_error || "Error creating new threat. Try again.",
                'error'
              );
            }
          }}
        >+ {t?.ui?.add_threat || 'Add Threat'}</button>
        <button
          type="button"
          style={{ padding: '10px 30px', fontSize: '16px', background: '#ffa833', color: '#00243c', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
          onClick={async () => {
            if (!threats || !Array.isArray(threats)) {
              showNotification(
                t?.ui?.no_threats_title || "No Data",
                "No hay amenazas para actualizar.",
                'warning'
              );
              return;
            }
            try {
              const updates = threats.map(threat => {
                // Usar el estado actual de React en lugar de leer del DOM
                const residualRiskValue = getResidualRiskValue(threat.id);
                
                return {
                  threat_id: threat.id,
                  title: document.getElementById(`title-${threat.id}`)?.value ?? threat.title,
                  type: document.getElementById(`type-${threat.id}`)?.value ?? threat.type,
                  description: document.getElementById(`description-${threat.id}`)?.value ?? threat.description,
                  remediation: { 
                    description: document.getElementById(`remediation-${threat.id}`)?.value ?? threat.remediation?.description ?? "",
                    status: threat.remediation?.status ?? false // Usar el estado de React directamente
                  },
                  // Incluir el riesgo residual en el payload principal
                  residual_risk: residualRiskValue,
                  // Usar los datos OWASP del estado de React (que se actualizan con los selectors)
                  skill_level: threat.risk?.skill_level ?? 0,
                  motive: threat.risk?.motive ?? 0,
                  opportunity: threat.risk?.opportunity ?? 0,
                  size: threat.risk?.size ?? 0,
                  ease_of_discovery: threat.risk?.ease_of_discovery ?? 0,
                  ease_of_exploit: threat.risk?.ease_of_exploit ?? 0,
                  awareness: threat.risk?.awareness ?? 0,
                  intrusion_detection: threat.risk?.intrusion_detection ?? 0,
                  loss_of_confidentiality: threat.risk?.loss_of_confidentiality ?? 0,
                  loss_of_integrity: threat.risk?.loss_of_integrity ?? 0,
                  loss_of_availability: threat.risk?.loss_of_availability ?? 0,
                  loss_of_accountability: threat.risk?.loss_of_accountability ?? 0,
                  financial_damage: threat.risk?.financial_damage ?? 0,
                  reputation_damage: threat.risk?.reputation_damage ?? 0,
                  non_compliance: threat.risk?.non_compliance ?? 0,
                  privacy_violation: threat.risk?.privacy_violation ?? 0,
                };
              });
              console.log("Updates payload:", updates);
              // Actualizar todos los datos incluyendo riesgo residual en una sola llamada
              await updateThreatsRiskBatch(id, updates);
              
              // Borrar en backend los threats eliminados
              let deletionErrors = [];
              for (const threatId of deletedThreats) {
                try {
                  console.log(`Intentando borrar threat con ID: ${threatId}`);
                  await axios.delete(`http://localhost:8000/threat/${threatId}`);
                  console.log(`Threat ${threatId} borrado exitosamente`);
                } catch (error) {
                  console.error(`Error borrando threat ${threatId}:`, error);
                  deletionErrors.push(`${threatId}: ${error.response?.data?.detail || error.message}`);
                }
              }
              
              if (deletionErrors.length > 0) {
                showNotification(
                  t?.ui?.partial_success_title || "Partial Success",
                  t?.ui?.partial_success || `Actualización completada, pero hubo errores al borrar algunos threats:\n${deletionErrors.join('\n')}`,
                  'warning'
                );
              } else {
                showNotification(
                  t?.ui?.update_success_title || "Success!",
                  "Todos los valores han sido actualizados y los eliminados borrados",
                  'success'
                );
              }
              setDeletedThreats([]);
              
            } catch (error) {
              showNotification(
                t?.ui?.save_error_title || "Error",
                "Ocurrió un error al guardar los valores. Verifica los datos e intenta de nuevo.",
                'error'
              );
              console.error(error);
            }
          }}
        >{t?.ui?.save_all || 'Save All'}</button>
      </div>

      {/* Modal para mostrar la imagen en tamaño completo */}
      <Modal isOpen={isOpen} onClose={onClose} size="6xl" isCentered>
        <ModalOverlay bg="blackAlpha.800" />
        <ModalContent maxW="90vw" maxH="90vh" bg="transparent" boxShadow="none">
          <ModalCloseButton 
            color="white" 
            bg="blackAlpha.600" 
            _hover={{ bg: "blackAlpha.800" }}
            size="lg"
            top={2}
            right={2}
            zIndex={2}
          />
          <ModalBody p={0} display="flex" justifyContent="center" alignItems="center">
            <ChakraImage
              src={`http://localhost:8000/diagrams/${serviceData.diagram}`}
              alt={serviceData.title}
              maxW="100%"
              maxH="100%"
              objectFit="contain"
              borderRadius="md"
            />
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  );
}
export default Analysis;