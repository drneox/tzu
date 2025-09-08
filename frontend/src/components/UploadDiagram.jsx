import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { 
  Flex, 
  Box, 
  Input, 
  Button, 
  Heading, 
  Text, 
  Progress, 
  Spinner,
  VStack,
  Icon,
  useColorModeValue,
} from "@chakra-ui/react";
import { FiUpload, FiCheck, FiAlertCircle } from "react-icons/fi";
import { uploadDiagram } from "../services";
import { keyframes } from "@emotion/react"; // 👈 keyframes viene de Emotion

// Animaciones personalizadas
const bounce = keyframes`
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const UploadDiagram = () => {
  const { id } = useParams();
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState(null); // 'success', 'warning', 'error', null
  const [errorMessage, setErrorMessage] = useState(""); // Para mostrar mensajes específicos del backend
  const navigate = useNavigate();
  
  const bgColor = useColorModeValue("white", "gray.800");
  const borderColor = useColorModeValue("gray.200", "gray.600");

  const simulateProgress = () => {
    setUploadProgress(0);
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 90) {
          clearInterval(interval);
          return 90;
        }
        return prev + Math.random() * 15;
      });
    }, 200);
    return interval;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    
    setIsUploading(true);
    setUploadStatus(null);
    
    const progressInterval = simulateProgress();
    
    try {
      console.log("Enviando diagrama al servidor...");
      const response = await uploadDiagram(id, file);
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      console.log("Respuesta del servidor:", response.data);
      console.log("¿La respuesta indica éxito?", response.data.success);
      console.log("Mensaje de la respuesta:", response.data.message);
      console.log("Datos del information_system:", response.data.information_system);
      
      if (response.data.success) {
        console.log("La respuesta indica ÉXITO - estableciendo estado a 'success'");
        setUploadStatus('success');
        
        // Redirigir automáticamente al análisis después de un breve retraso
        setTimeout(() => {
          console.log("Redirigiendo al análisis de amenazas...");
          navigate(`/analysis/${id}`);
        }, 2000);
      } else {
        // Si no hay amenazas o hubo problemas, mostrar como warning y usar el mensaje del servidor
        console.log("La respuesta indica FRACASO - estableciendo estado a 'warning'");
        setUploadStatus('warning');
        // Guardamos el mensaje específico del backend
        setErrorMessage(response.data.message || "No se encontraron amenazas en el diagrama");
        console.log("Mensaje de error establecido:", response.data.message);
      }
    } catch (error) {
      clearInterval(progressInterval);
      setUploadStatus('error');
      setIsUploading(false);
      setErrorMessage(error.response?.data?.message || "Error al conectar con el servidor");
      console.error("Error al subir el diagrama:", error);
    }
  };

  const resetUpload = () => {
    setFile(null);
    setIsUploading(false);
    setUploadProgress(0);
    setUploadStatus(null);
    setErrorMessage("");
  };

  return (
    <Flex align="center" justify="center" height="100vh" bg="gray.50" p={4}>
      <Box 
        p={8} 
        borderWidth={1} 
        borderRadius={16} 
        boxShadow="2xl" 
        width="500px"
        bg={bgColor}
        borderColor={borderColor}
        animation={`${fadeIn} 0.5s ease-out`}
      >
        <VStack spacing={6}>
          <Heading size="lg" textAlign="center" color="teal.600">
            <Icon as={FiUpload} mr={2} />
            Subir Diagrama de Amenazas
          </Heading>

          {!isUploading && uploadStatus !== 'success' && (
            <Box
              p={6}
              border="2px dashed"
              borderColor={file ? "teal.300" : "gray.300"}
              borderRadius={12}
              width="100%"
              textAlign="center"
              transition="all 0.3s"
              _hover={{
                borderColor: "teal.400",
                transform: "scale(1.02)",
              }}
              bg={file ? "teal.50" : "gray.50"}
            >
              <Input
                type="file"
                accept="image/*"
                onChange={e => setFile(e.target.files[0])}
                required
                display="none"
                id="file-upload"
              />
              <label htmlFor="file-upload" style={{ cursor: 'pointer', width: '100%', display: 'block' }}>
                <Icon 
                  as={FiUpload} 
                  size="3em" 
                  color={file ? "teal.500" : "gray.400"} 
                  mb={3}
                  animation={file ? `${bounce} 1s infinite` : undefined}
                />
                <Text fontSize="lg" color={file ? "teal.600" : "gray.500"} mb={2}>
                  {file ? file.name : "Haz clic aquí o arrastra tu diagrama"}
                </Text>
                <Text fontSize="sm" color="gray.400">
                  Formatos soportados: JPG, PNG, SVG
                </Text>
              </label>
            </Box>
          )}

          {isUploading && (
            <VStack spacing={4} width="100%" animation={`${fadeIn} 0.3s ease-out`}>
              <Box textAlign="center">
                <Spinner
                  thickness="4px"
                  speed="0.65s"
                  emptyColor="gray.200"
                  color="teal.500"
                  size="xl"
                  animation={`${pulse} 2s infinite`}
                />
                <Text mt={4} fontSize="lg" color="teal.600" fontWeight="medium">
                  {uploadProgress < 30 ? "Procesando imagen..." : 
                   uploadProgress < 60 ? "Analizando diagrama..." :
                   uploadProgress < 90 ? "Generando amenazas..." :
                   "Finalizando..."}
                </Text>
              </Box>
              
              <Box width="100%">
                <Progress 
                  value={uploadProgress} 
                  colorScheme="teal" 
                  size="lg" 
                  hasStripe 
                  isAnimated
                  borderRadius="full"
                />
                <Text textAlign="center" fontSize="sm" color="gray.500" mt={2}>
                  {Math.round(uploadProgress)}% completado
                </Text>
              </Box>
              
              <Text fontSize="sm" color="gray.600" textAlign="center">
                🤖 IA analizando tu diagrama para identificar posibles amenazas...
              </Text>
            </VStack>
          )}

          {uploadStatus === 'success' && (
            <VStack spacing={4} animation={`${fadeIn} 0.5s ease-out`}>
              <Icon as={FiCheck} size="4em" color="green.500" animation={`${bounce} 0.6s ease-out`} />
              <Text fontSize="xl" color="green.600" fontWeight="bold" textAlign="center">
                ¡Diagrama procesado exitosamente! 🎉
              </Text>
              <Text fontSize="md" color="gray.600" textAlign="center">
                Redirigiendo al análisis de amenazas...
              </Text>
              <Progress size="xs" isIndeterminate colorScheme="green" width="200px" />
            </VStack>
          )}

          {uploadStatus === 'warning' && (
            <VStack spacing={4} animation={`${fadeIn} 0.3s ease-out`}>
              <Icon as={FiAlertCircle} size="3em" color="orange.500" />
              <Text fontSize="lg" color="orange.600" fontWeight="medium">
                Aviso
              </Text>
              <Text fontSize="sm" color="gray.600" textAlign="center">
                {errorMessage || "No se encontraron amenazas en el diagrama"}
              </Text>
              <Button onClick={resetUpload} colorScheme="orange" variant="outline">
                Intentar de nuevo
              </Button>
            </VStack>
          )}
          
          {uploadStatus === 'error' && (
            <VStack spacing={4} animation={`${fadeIn} 0.3s ease-out`}>
              <Icon as={FiAlertCircle} size="3em" color="red.500" />
              <Text fontSize="lg" color="red.600" fontWeight="medium">
                Error al procesar el diagrama
              </Text>
              <Text fontSize="sm" color="gray.600" textAlign="center">
                Se ha producido un error durante el procesamiento.
                Por favor, verifica que la imagen sea válida e intenta nuevamente.
              </Text>
              <Button onClick={resetUpload} colorScheme="red" variant="outline">
                Intentar de nuevo
              </Button>
            </VStack>
          )}

          {file && !isUploading && uploadStatus !== 'success' && (
            <VStack spacing={3} width="100%">
              <Button 
                onClick={handleSubmit} 
                colorScheme="teal" 
                size="lg" 
                width="full"
                leftIcon={<FiUpload />}
                _hover={{
                  transform: "translateY(-2px)",
                  boxShadow: "lg"
                }}
                transition="all 0.2s"
              >
                Analizar Diagrama
              </Button>
              <Button 
                onClick={resetUpload} 
                variant="ghost" 
                size="sm"
                color="gray.500"
              >
                Seleccionar otro archivo
              </Button>
            </VStack>
          )}
        </VStack>
      </Box>
    </Flex>
  );
};

export default UploadDiagram;
