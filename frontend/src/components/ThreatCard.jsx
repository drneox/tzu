import React from 'react';
import {
  Box,
  VStack,
  HStack,
  Text,
  Button,
  Collapse,
  Textarea,
  useColorModeValue,
  Flex,
} from '@chakra-ui/react';
import { FaTrash, FaEdit, FaEye, FaEyeSlash } from 'react-icons/fa';
import RiskDisplay from './RiskDisplay';
import OwaspSelector from './OwaspSelector';
import { calculateTextareaHeight } from '../utils/textareaHelpers';
import { useLocalization } from '../hooks/useLocalization';

/**
 * ThreatCard component - Individual threat card with OWASP risk assessment
 */
const ThreatCard = ({
  threat,
  inherentRisk,
  residualRisk,
  currentRisk,
  isEditing,
  isCollapsed,
  remediationValue,
  onOwaspChange,
  onToggleEdit,
  onToggleCollapse,
  onRemediationChange,
  onThreatUpdate,
  onThreatDelete,
  renderTypeBadges,
  createRemediationSwitch
}) => {
  const { t } = useLocalization();
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  return (
    <Box
      p={6}
      shadow="md"
      borderWidth="1px"
      borderColor={borderColor}
      borderRadius="md"
      bg={cardBg}
      position="relative"
    >
      {/* Header */}
      <Flex align="center" mb={4}>
        <VStack align="start" spacing={1} flex={1}>
          <HStack>
            <Text fontSize="lg" fontWeight="bold">
              {threat.title}
            </Text>
            {threat.type && renderTypeBadges(threat.type)}
          </HStack>
          <Text fontSize="sm" color="gray.600">
            ID: {threat.id}
          </Text>
        </VStack>
        
        <HStack spacing={2}>
          <Button
            size="sm"
            colorScheme="blue"
            variant="ghost"
            leftIcon={isCollapsed ? <FaEye /> : <FaEyeSlash />}
            onClick={() => onToggleCollapse(threat.id)}
          >
            {isCollapsed ? t?.ui?.show || 'Show' : t?.ui?.hide || 'Hide'}
          </Button>
          <Button
            size="sm"
            colorScheme="yellow"
            variant="ghost"
            leftIcon={<FaEdit />}
            onClick={() => onToggleEdit(threat.id)}
          >
            {isEditing ? t?.ui?.cancel || 'Cancel' : t?.ui?.edit || 'Edit'}
          </Button>
          <Button
            size="sm"
            colorScheme="red"
            variant="ghost"
            leftIcon={<FaTrash />}
            onClick={() => onThreatDelete(threat.id)}
          >
            {t?.ui?.delete || 'Delete'}
          </Button>
        </HStack>
      </Flex>

      {/* Risk Summary */}
      <VStack spacing={2} align="stretch">
        <HStack justify="space-between" align="center" wrap="wrap">
          <HStack minW="150px">
            <Text fontSize="sm" minW="60px">
              <strong>{t?.ui?.inherent_risk || 'IR'}:</strong>
            </Text>
            <RiskDisplay 
              riskValue={inherentRisk} 
              variant="badge" 
              size="sm" 
              showLabel={false}
            />
          </HStack>
          
          <HStack minW="150px">
            <Text fontSize="sm" minW="60px">
              <strong>{t?.ui?.residual_risk || 'RR'}:</strong>
            </Text>
            <RiskDisplay 
              riskValue={residualRisk} 
              variant="badge" 
              size="sm" 
              showLabel={false}
            />
          </HStack>
          
          <HStack minW="150px">
            <Text fontSize="sm" minW="60px">
              <strong>{t?.ui?.current_risk || 'CR'}:</strong>
            </Text>
            <RiskDisplay 
              riskValue={currentRisk} 
              variant="badge" 
              size="sm" 
              showLabel={false}
            />
          </HStack>
        </HStack>
        
        <HStack justify="center" align="center">
          <Text fontSize="sm">
            <strong>{t?.ui?.remediation || 'Remediation'}:</strong>
          </Text>
          {createRemediationSwitch(threat, "sm")}
        </HStack>
      </VStack>

      {/* Collapsible Content */}
      <Collapse in={!isCollapsed}>
        <VStack spacing={4} mt={4} align="stretch">
          
          {/* Description */}
          <Box>
            <Text fontSize="sm" fontWeight="bold" mb={2}>
              {t?.ui?.description || 'Description'}:
            </Text>
            {isEditing ? (
              <Textarea
                value={threat.description || ''}
                onChange={(e) => onThreatUpdate(threat.id, 'description', e.target.value)}
                placeholder={t?.ui?.enter_description || "Enter description"}
                minH={calculateTextareaHeight(threat.description)}
              />
            ) : (
              <Text fontSize="sm" color="gray.700" whiteSpace="pre-wrap">
                {threat.description || t?.ui?.no_description || 'No description available'}
              </Text>
            )}
          </Box>

          {/* STRIDE Categories */}
          {threat.stride_categories && (
            <Box>
              <Text fontSize="sm" fontWeight="bold" mb={2}>
                STRIDE:
              </Text>
              <Text fontSize="sm" color="gray.700">
                {threat.stride_categories}
              </Text>
            </Box>
          )}

          {/* OWASP Risk Factors */}
          <Box>
            <Text fontSize="sm" fontWeight="bold" mb={3}>
              {t?.ui?.owasp_factors || 'OWASP Risk Factors'}:
            </Text>
            
            {/* Likelihood Factors */}
            <Text fontSize="xs" fontWeight="semibold" color="blue.600" mb={2}>
              {t?.ui?.likelihood || 'Likelihood'} - {t?.ui?.threat_agent_factors || 'Threat Agent Factors'}:
            </Text>
            <HStack spacing={2} wrap="wrap" mb={3}>
              <OwaspSelector threatId={threat.id} factorName="skill_level" currentValue={threat.skill_level} onChange={onOwaspChange} />
              <OwaspSelector threatId={threat.id} factorName="motive" currentValue={threat.motive} onChange={onOwaspChange} />
              <OwaspSelector threatId={threat.id} factorName="opportunity" currentValue={threat.opportunity} onChange={onOwaspChange} />
              <OwaspSelector threatId={threat.id} factorName="size" currentValue={threat.size} onChange={onOwaspChange} />
            </HStack>

            <Text fontSize="xs" fontWeight="semibold" color="blue.600" mb={2}>
              {t?.ui?.likelihood || 'Likelihood'} - {t?.ui?.vulnerability_factors || 'Vulnerability Factors'}:
            </Text>
            <HStack spacing={2} wrap="wrap" mb={4}>
              <OwaspSelector threatId={threat.id} factorName="ease_of_discovery" currentValue={threat.ease_of_discovery} onChange={onOwaspChange} />
              <OwaspSelector threatId={threat.id} factorName="ease_of_exploit" currentValue={threat.ease_of_exploit} onChange={onOwaspChange} />
              <OwaspSelector threatId={threat.id} factorName="awareness" currentValue={threat.awareness} onChange={onOwaspChange} />
              <OwaspSelector threatId={threat.id} factorName="intrusion_detection" currentValue={threat.intrusion_detection} onChange={onOwaspChange} />
            </HStack>

            {/* Impact Factors */}
            <Text fontSize="xs" fontWeight="semibold" color="red.600" mb={2}>
              {t?.ui?.impact || 'Impact'} - {t?.ui?.technical_impact || 'Technical Impact'}:
            </Text>
            <HStack spacing={2} wrap="wrap" mb={3}>
              <OwaspSelector threatId={threat.id} factorName="loss_of_confidentiality" currentValue={threat.loss_of_confidentiality} onChange={onOwaspChange} />
              <OwaspSelector threatId={threat.id} factorName="loss_of_integrity" currentValue={threat.loss_of_integrity} onChange={onOwaspChange} />
              <OwaspSelector threatId={threat.id} factorName="loss_of_availability" currentValue={threat.loss_of_availability} onChange={onOwaspChange} />
              <OwaspSelector threatId={threat.id} factorName="loss_of_accountability" currentValue={threat.loss_of_accountability} onChange={onOwaspChange} />
            </HStack>

            <Text fontSize="xs" fontWeight="semibold" color="red.600" mb={2}>
              {t?.ui?.impact || 'Impact'} - {t?.ui?.business_impact || 'Business Impact'}:
            </Text>
            <HStack spacing={2} wrap="wrap">
              <OwaspSelector threatId={threat.id} factorName="financial_damage" currentValue={threat.financial_damage} onChange={onOwaspChange} />
              <OwaspSelector threatId={threat.id} factorName="reputation_damage" currentValue={threat.reputation_damage} onChange={onOwaspChange} />
              <OwaspSelector threatId={threat.id} factorName="non_compliance" currentValue={threat.non_compliance} onChange={onOwaspChange} />
              <OwaspSelector threatId={threat.id} factorName="privacy_violation" currentValue={threat.privacy_violation} onChange={onOwaspChange} />
            </HStack>
          </Box>

        </VStack>
      </Collapse>
    </Box>
  );
};

export default ThreatCard;
