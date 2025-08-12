import axios from "axios";
import { FaTrash } from "react-icons/fa";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Flex, TableContainer, Table, Tr, Td, Thead, Th, Tbody } from "@chakra-ui/react";
import { Box } from "@chakra-ui/react";
import { fetchInformationSystemById, updateThreatsRiskBatch, createThreatForSystem } from "../services/index";

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

// Función para calcular el riesgo inherente (promedio de DREADC)
const calculateInherentRisk = (risk) => {
  if (!risk) return 0;
  const values = [
    risk.damage || 0,
    risk.reproducibility || 0,
    risk.exploitability || 0,
    risk.affected_users || 0,
    risk.discoverability || 0,
    risk.compliance || 0
  ];
  const sum = values.reduce((acc, val) => acc + val, 0);
  const average = sum / values.length;
  return average.toFixed(2);
};

// Función para obtener el color del riesgo inherente según su valor
const getRiskColor = (riskValue) => {
  const value = parseFloat(riskValue);
  if (value <= 2) return "#38a169"; // Verde (bajo)
  if (value <= 3.5) return "#d69e2e"; // Amarillo (medio)
  return "#e53e3e"; // Rojo (alto)
};

const Analysis = () => {
  const [isLoading, setIsLoading] = useState(true);
  const { id } = useParams();
  const [serviceData, setServiceData] = useState(null);
  const [deletedThreats, setDeletedThreats] = useState([]);
  const [inherentRisks, setInherentRisks] = useState({});
  
  const fetchData = async () => {
    setIsLoading(true);
    const data = await fetchInformationSystemById(id);
    setServiceData(data);
    
    // Inicializar los riesgos inherentes
    if (data && data.threats) {
      const initialRisks = {};
      data.threats.forEach(threat => {
        initialRisks[threat.id] = calculateInherentRisk(threat.risk);
      });
      setInherentRisks(initialRisks);
    }
    
    setIsLoading(false);
  };
  
  // Función para actualizar el riesgo inherente cuando cambian los valores DREADC
  const updateInherentRisk = (threatId) => {
    const damage = Number(document.getElementById(`damage-${threatId}`)?.value || 0);
    const reproducibility = Number(document.getElementById(`reproducibility-${threatId}`)?.value || 0);
    const exploitability = Number(document.getElementById(`exploitability-${threatId}`)?.value || 0);
    const affected_users = Number(document.getElementById(`affected_users-${threatId}`)?.value || 0);
    const discoverability = Number(document.getElementById(`discoverability-${threatId}`)?.value || 0);
    const compliance = Number(document.getElementById(`compliance-${threatId}`)?.value || 0);
    
    const values = [damage, reproducibility, exploitability, affected_users, discoverability, compliance];
    const sum = values.reduce((acc, val) => acc + val, 0);
    const average = sum / values.length;
    
    setInherentRisks(prev => ({
      ...prev,
      [threatId]: average.toFixed(2)
    }));
  };
  
  useEffect(() => {
    fetchData();
  }, [id]);
  
  if (isLoading || !serviceData){
    return (
        <div className="App">
          <h1>Cargando...</h1>
        </div>
      );
  }
  return (
    <Flex
      as="nav"
      align="center"
      wrap="wrap"
      padding="0.5rem"
      justify="center"
      style={{ marginBottom: "160px" }}
    >
      <Box>
        <h1>Titulo:{serviceData.title}</h1>
        <h2>Descripción:{serviceData.description}</h2>
        <h2>Diagrama:</h2>
        <img src={`http://localhost:8000/diagrams/${serviceData.diagram}`} alt={serviceData.title} />
        <h2>Amenazas:</h2>
      </Box>
      <TableContainer>
        <Table border="2px solid gray" borderCollapse="collapse" variant='striped' colorScheme='gray' overflowX='auto' whiteSpace='normal'>
          <Thead>
            <Tr bg="gray.300" color="white" p="4">
              <Th p="4" shadow="md">Titulo</Th>
              <Th  p="4" shadow="md" maxWidth='100px'>Tipo</Th>
              <Th  p="4" shadow="md">Descripción</Th>
              <Th  p="4" shadow="md" maxWidth='200px'>Remediación</Th>
              <Th  p="4" shadow="md">D</Th>
              <Th  p="4" shadow="md" maxWidth='100px'>R</Th>
              <Th  p="4" shadow="md" maxWidth='100px'>E</Th>
              <Th  p="4" shadow="md" maxWidth='100px'>A</Th>
              <Th  p="4" shadow="md" maxWidth='100px'>D</Th>
              <Th  p="4" shadow="md" maxWidth='100px'>C</Th>
              <Th  p="4" shadow="md" maxWidth='100px'>Riesgo Inherente</Th>
              <Th  p="4" shadow="md" maxWidth='100px'>Aplicada</Th>
              <Th  p="4" shadow="md" maxWidth='100px'>Borrar</Th>
            </Tr>
          </Thead>
          <Tbody>
            {serviceData.threats.map((threat) => (
              <Tr key={threat.id} style={{ backgroundColor: threat.id.toString().startsWith('temp-') ? '#f0fff4' : 'transparent' }}>
                
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
                <Td p="4" shadow="md" style={{width: "30px", minWidth: "30px"}}>
                  <input 
                    type="text" 
                    defaultValue={threat.risk.damage} 
                    style={{width: "30px"}} 
                    id={`damage-${threat.id}`}
                    onChange={() => updateInherentRisk(threat.id)}
                  />
                </Td>
                <Td p="4" shadow="md" style={{width: "30px", minWidth: "30px"}}>
                  <input 
                    type="text" 
                    defaultValue={threat.risk.reproducibility} 
                    style={{width: "30px"}} 
                    id={`reproducibility-${threat.id}`}
                    onChange={() => updateInherentRisk(threat.id)}
                  />
                </Td>
                <Td p="4" shadow="md" style={{width: "30px", minWidth: "30px"}}>
                  <input 
                    type="text" 
                    defaultValue={threat.risk.exploitability} 
                    style={{width: "30px"}} 
                    id={`exploitability-${threat.id}`}
                    onChange={() => updateInherentRisk(threat.id)}
                  />
                </Td>
                <Td p="4" shadow="md" style={{width: "30px", minWidth: "30px"}}>
                  <input 
                    type="text" 
                    defaultValue={threat.risk.affected_users} 
                    style={{width: "30px"}} 
                    id={`affected_users-${threat.id}`}
                    onChange={() => updateInherentRisk(threat.id)}
                  />
                </Td>
                <Td p="4" shadow="md" style={{width: "30px", minWidth: "30px"}}>
                  <input 
                    type="text" 
                    defaultValue={threat.risk.discoverability} 
                    style={{width: "30px"}} 
                    id={`discoverability-${threat.id}`}
                    onChange={() => updateInherentRisk(threat.id)}
                  />
                </Td>
                <Td p="4" shadow="md" style={{width: "30px", minWidth: "30px"}}>
                  <input 
                    type="text" 
                    defaultValue={threat.risk.compliance} 
                    style={{width: "30px"}} 
                    id={`compliance-${threat.id}`}
                    onChange={() => updateInherentRisk(threat.id)}
                  />
                </Td>
                <Td p="4" shadow="md" style={{width: "60px", minWidth: "60px", textAlign: "center", backgroundColor: "#f7fafc"}}>
                  <span style={{
                    fontWeight: "bold", 
                    color: getRiskColor(inherentRisks[threat.id] || calculateInherentRisk(threat.risk)), 
                    fontSize: "14px"
                  }}>
                    {inherentRisks[threat.id] || calculateInherentRisk(threat.risk)}
                  </span>
                </Td>
                <Td p="4" shadow="md" style={{width: "80px", minWidth: "80px"}}>
                  <select 
                    key={`status-${threat.id}-${threat.remediation?.status}`}
                    defaultValue={threat.remediation?.status === true ? "true" : "false"} 
                    style={{width: "80px", padding: "2px"}} 
                    id={`status-${threat.id}`}
                  >
                    <option value="true">Sí</option>
                    <option value="false">No</option>
                  </select>
                </Td>
                <Td p="4" shadow="md">
                  <button
                    type="button"
                    style={{ background: '#e2e8f0', color: '#2d3748', border: 'none', borderRadius: '4px', padding: '4px 10px', cursor: 'pointer' }}
                    aria-label="Eliminar amenaza"
                    title="Eliminar amenaza"
                    onClick={() => {
                      setDeletedThreats(prev => prev.includes(threat.id) ? prev : [...prev, threat.id]);
                      setServiceData(prev => {
                        const newThreats = prev.threats.filter(t => t.id !== threat.id);
                        return { ...prev, threats: newThreats };
                      });
                    }}
                  ><FaTrash size={20} /></button>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </TableContainer>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '15px', marginTop: '20px' }}>
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
              
              // Agregar el nuevo threat al estado local
              setServiceData(prev => ({
                ...prev,
                threats: [...prev.threats, createdThreat]
              }));
              
              // Inicializar el riesgo inherente para el nuevo threat
              setInherentRisks(prev => ({
                ...prev,
                [createdThreat.id]: calculateInherentRisk(createdThreat.risk)
              }));
              
              alert("Nueva amenaza agregada exitosamente");
            } catch (error) {
              console.error("Error creando nueva amenaza:", error);
              alert("Error al crear la nueva amenaza. Intenta de nuevo.");
            }
          }}
        >+ Agregar Amenaza</button>
        <button
          type="button"
          style={{ padding: '10px 30px', fontSize: '16px', background: '#ffa833', color: '#00243c', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
          onClick={async () => {
            if (!serviceData.threats || !Array.isArray(serviceData.threats)) {
              alert("No hay amenazas para actualizar.");
              return;
            }
            try {
              const updates = serviceData.threats.map(threat => {
                const statusValue = document.getElementById(`status-${threat.id}`)?.value;
                const statusBoolean = statusValue === "true";
                console.log(`Threat ${threat.id}: status select value = "${statusValue}", converted to boolean = ${statusBoolean}`);
                
                return {
                  threat_id: threat.id,
                  title: document.getElementById(`title-${threat.id}`)?.value ?? "",
                  type: document.getElementById(`type-${threat.id}`)?.value ?? "",
                  description: document.getElementById(`description-${threat.id}`)?.value ?? "",
                  remediation: { 
                    description: document.getElementById(`remediation-${threat.id}`)?.value ?? "",
                    status: statusBoolean
                  },
                  damage: Number(document.getElementById(`damage-${threat.id}`)?.value ?? 0),
                  reproducibility: Number(document.getElementById(`reproducibility-${threat.id}`)?.value ?? 0),
                  exploitability: Number(document.getElementById(`exploitability-${threat.id}`)?.value ?? 0),
                  affected_users: Number(document.getElementById(`affected_users-${threat.id}`)?.value ?? 0),
                  discoverability: Number(document.getElementById(`discoverability-${threat.id}`)?.value ?? 0),
                  compliance: Number(document.getElementById(`compliance-${threat.id}`)?.value ?? 0),
                };
              });
              console.log("Updates payload:", updates);
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
                alert(`Actualización completada, pero hubo errores al borrar algunos threats:\n${deletionErrors.join('\n')}`);
              } else {
                alert("Todos los valores han sido actualizados y los eliminados borrados");
              }
              setDeletedThreats([]);
              
              // Hacer fetch automático para sincronizar con el backend
              console.log("Refrescando datos después del guardado...");
              await fetchData();
              console.log("Datos refrescados");
            } catch (error) {
              alert("Ocurrió un error al guardar los valores. Verifica los datos e intenta de nuevo.");
              console.error(error);
            }
          }}
        >Guardar todos</button>
      </div>
    </Flex>
  );
}
export default Analysis;