import { useState, useRef } from "react";
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
  HStack,
  Icon,
  Textarea,
  useColorModeValue,
} from "@chakra-ui/react";
import { FiUpload, FiCheck, FiAlertCircle, FiFileText, FiImage } from "react-icons/fi";
import { uploadDiagram, uploadDiagramText } from "../services";
import { keyframes } from "@emotion/react";

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

const ACCEPTED_FILES =
  "image/*,.pdf,.xml,.json,.md,.txt,.svg";

const FILE_HINT =
  "Formatos soportados: JPG, PNG, SVG, PDF, XML, JSON, TXT, MD";

const UploadDiagram = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  // 'file' | 'text'
  const [mode, setMode] = useState("file");

  // file-mode state
  const [file, setFile] = useState(null);

  // text-mode state
  const [textContent, setTextContent] = useState("");

  // shared upload state
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState(null); // 'success' | 'warning' | 'error' | null
  const [errorMessage, setErrorMessage] = useState("");

  const fileInputRef = useRef(null);

  const bgColor = useColorModeValue("white", "gray.800");
  const borderColor = useColorModeValue("gray.200", "gray.600");
  const tabActiveBg = useColorModeValue("indigo.50", "indigo.900");
  const tabInactiveBg = useColorModeValue("gray.50", "gray.700");

  const simulateProgress = () => {
    setUploadProgress(0);
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
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

    const readyFile = mode === "file" && file;
    const readyText = mode === "text" && textContent.trim().length > 0;
    if (!readyFile && !readyText) return;

    setIsUploading(true);
    setUploadStatus(null);
    setErrorMessage("");

    const progressInterval = simulateProgress();

    try {
      let response;
      if (mode === "file") {
        response = await uploadDiagram(id, file);
      } else {
        response = await uploadDiagramText(id, textContent.trim());
      }

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (response.data.success) {
        setUploadStatus("success");
        setTimeout(() => navigate(`/analysis/${id}`), 2000);
      } else {
        setUploadStatus("warning");
        setErrorMessage(
          response.data.message || "No se encontraron amenazas en el contenido analizado"
        );
      }
    } catch (error) {
      clearInterval(progressInterval);
      setUploadStatus("error");
      setIsUploading(false);
      setErrorMessage(
        error.response?.data?.message || "Error al conectar con el servidor"
      );
    }
  };

  const resetUpload = () => {
    setFile(null);
    setTextContent("");
    setIsUploading(false);
    setUploadProgress(0);
    setUploadStatus(null);
    setErrorMessage("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const isReady =
    !isUploading &&
    uploadStatus !== "success" &&
    (mode === "file" ? !!file : textContent.trim().length > 0);

  const progressLabel =
    uploadProgress < 30
      ? mode === "file"
        ? "Procesando archivo..."
        : "Procesando texto..."
      : uploadProgress < 60
      ? "Analizando contenido..."
      : uploadProgress < 90
      ? "Generando amenazas..."
      : "Finalizando...";

  return (
    <Flex align="center" justify="center" minHeight="100vh" bg="gray.50" p={4}>
      <Box
        p={8}
        borderWidth={1}
        borderRadius={16}
        boxShadow="2xl"
        width="520px"
        bg={bgColor}
        borderColor={borderColor}
        animation={`${fadeIn} 0.5s ease-out`}
      >
        <VStack spacing={6}>
          <Heading size="lg" textAlign="center" color="indigo.600">
            <Icon as={FiUpload} mr={2} />
            Subir Diagrama de Amenazas
          </Heading>

          {/* ── TABS ── */}
          {!isUploading && uploadStatus !== "success" && (
            <HStack width="100%" spacing={0} borderRadius={10} overflow="hidden" border="1px solid" borderColor="gray.200">
              <Button
                flex={1}
                borderRadius={0}
                leftIcon={<FiImage />}
                bg={mode === "file" ? tabActiveBg : tabInactiveBg}
                color={mode === "file" ? "indigo.700" : "gray.500"}
                fontWeight={mode === "file" ? "bold" : "normal"}
                borderRight="1px solid"
                borderColor="gray.200"
                _hover={{ bg: tabActiveBg, color: "indigo.700" }}
                onClick={() => { setMode("file"); resetUpload(); }}
                size="sm"
                py={5}
              >
                Archivo / Imagen
              </Button>
              <Button
                flex={1}
                borderRadius={0}
                leftIcon={<FiFileText />}
                bg={mode === "text" ? tabActiveBg : tabInactiveBg}
                color={mode === "text" ? "indigo.700" : "gray.500"}
                fontWeight={mode === "text" ? "bold" : "normal"}
                _hover={{ bg: tabActiveBg, color: "indigo.700" }}
                onClick={() => { setMode("text"); resetUpload(); }}
                size="sm"
                py={5}
              >
                Descripción de Texto
              </Button>
            </HStack>
          )}

          {/* ── FILE MODE ── */}
          {mode === "file" && !isUploading && uploadStatus !== "success" && (
            <Box
              p={6}
              border="2px dashed"
              borderColor={file ? "indigo.300" : "gray.300"}
              borderRadius={12}
              width="100%"
              textAlign="center"
              transition="all 0.3s"
              _hover={{ borderColor: "indigo.400", transform: "scale(1.02)" }}
              bg={file ? "indigo.50" : "gray.50"}
            >
              <Input
                ref={fileInputRef}
                type="file"
                accept={ACCEPTED_FILES}
                onChange={(e) => setFile(e.target.files[0])}
                display="none"
                id="file-upload"
              />
              <label htmlFor="file-upload" style={{ cursor: "pointer", width: "100%", display: "block" }}>
                <Icon
                  as={FiUpload}
                  fontSize="3em"
                  color={file ? "indigo.500" : "gray.400"}
                  mb={3}
                  animation={file ? `${bounce} 1s infinite` : undefined}
                />
                <Text fontSize="lg" color={file ? "indigo.600" : "gray.500"} mb={2}>
                  {file ? file.name : "Haz clic aquí o arrastra tu archivo"}
                </Text>
                <Text fontSize="sm" color="gray.400">
                  {FILE_HINT}
                </Text>
              </label>
            </Box>
          )}

          {/* ── TEXT MODE ── */}
          {mode === "text" && !isUploading && uploadStatus !== "success" && (
            <Box width="100%">
              <Text fontSize="sm" color="gray.500" mb={2}>
                Describe la arquitectura del sistema, flujos de datos, componentes y conexiones.
                Cuanto más detallado, mejor será el análisis de amenazas.
              </Text>
              <Textarea
                placeholder={
                  "Ejemplo:\n" +
                  "El sistema tiene un cliente web que se conecta a una API REST. " +
                  "La API autentica usuarios con JWT y accede a una base de datos PostgreSQL. " +
                  "Los datos se transfieren mediante HTTPS. Existe un servicio de notificaciones por correo..."
                }
                value={textContent}
                onChange={(e) => setTextContent(e.target.value)}
                minH="200px"
                borderColor={textContent.trim() ? "indigo.300" : "gray.300"}
                focusBorderColor="indigo.400"
                resize="vertical"
                fontSize="sm"
                bg={textContent.trim() ? "indigo.50" : "gray.50"}
              />
              <Text fontSize="xs" color="gray.400" mt={1} textAlign="right">
                {textContent.length} caracteres
              </Text>
            </Box>
          )}

          {/* ── UPLOADING STATE ── */}
          {isUploading && (
            <VStack spacing={4} width="100%" animation={`${fadeIn} 0.3s ease-out`}>
              <Box textAlign="center">
                <Spinner
                  thickness="4px"
                  speed="0.65s"
                  emptyColor="gray.200"
                  color="indigo.500"
                  size="xl"
                  animation={`${pulse} 2s infinite`}
                />
                <Text mt={4} fontSize="lg" color="indigo.600" fontWeight="medium">
                  {progressLabel}
                </Text>
              </Box>
              <Box width="100%">
                <Progress
                  value={uploadProgress}
                  colorScheme="indigo"
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
                🤖 IA analizando el contenido para identificar posibles amenazas...
              </Text>
            </VStack>
          )}

          {/* ── SUCCESS STATE ── */}
          {uploadStatus === "success" && (
            <VStack spacing={4} animation={`${fadeIn} 0.5s ease-out`}>
              <Icon as={FiCheck} fontSize="4em" color="green.500" animation={`${bounce} 0.6s ease-out`} />
              <Text fontSize="xl" color="green.600" fontWeight="bold" textAlign="center">
                ¡Contenido procesado exitosamente! 🎉
              </Text>
              <Text fontSize="md" color="gray.600" textAlign="center">
                Redirigiendo al análisis de amenazas...
              </Text>
              <Progress size="xs" isIndeterminate colorScheme="green" width="200px" />
            </VStack>
          )}

          {/* ── WARNING STATE ── */}
          {uploadStatus === "warning" && (
            <VStack spacing={4} animation={`${fadeIn} 0.3s ease-out`}>
              <Icon as={FiAlertCircle} fontSize="3em" color="orange.500" />
              <Text fontSize="lg" color="orange.600" fontWeight="medium">
                Aviso
              </Text>
              <Text fontSize="sm" color="gray.600" textAlign="center">
                {errorMessage || "No se encontraron amenazas en el contenido analizado"}
              </Text>
              <Button onClick={resetUpload} colorScheme="indigo" variant="outline">
                Intentar de nuevo
              </Button>
            </VStack>
          )}

          {/* ── ERROR STATE ── */}
          {uploadStatus === "error" && (
            <VStack spacing={4} animation={`${fadeIn} 0.3s ease-out`}>
              <Icon as={FiAlertCircle} fontSize="3em" color="red.500" />
              <Text fontSize="lg" color="red.600" fontWeight="medium">
                Error al procesar el contenido
              </Text>
              <Text fontSize="sm" color="gray.600" textAlign="center">
                {errorMessage || "Se ha producido un error durante el procesamiento. Por favor intente nuevamente."}
              </Text>
              <Button onClick={resetUpload} colorScheme="red" variant="outline">
                Intentar de nuevo
              </Button>
            </VStack>
          )}

          {/* ── SUBMIT / RESET BUTTONS ── */}
          {isReady && (
            <VStack spacing={3} width="100%">
              <Button
                onClick={handleSubmit}
                colorScheme="indigo"
                size="lg"
                width="full"
                leftIcon={<FiUpload />}
                _hover={{ transform: "translateY(-2px)", boxShadow: "lg" }}
                transition="all 0.2s"
              >
                Analizar {mode === "file" ? "Archivo" : "Descripción"}
              </Button>
              <Button
                onClick={resetUpload}
                variant="ghost"
                size="sm"
                color="gray.500"
              >
                {mode === "file" ? "Seleccionar otro archivo" : "Limpiar texto"}
              </Button>
            </VStack>
          )}
        </VStack>
      </Box>
    </Flex>
  );
};

export default UploadDiagram;
