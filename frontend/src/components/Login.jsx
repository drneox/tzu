import React, { useState } from 'react';
import {
  Box,
  VStack,
  Image,
  Heading,
  Text,
  Input,
  Button,
  FormControl,
  FormLabel,
  Alert,
  AlertIcon,
  Card,
  CardBody,
  useColorModeValue,
  Flex,
  InputGroup,
  InputLeftElement,
  InputRightElement,
  IconButton,
  useToast
} from '@chakra-ui/react';
import { FaUser, FaLock, FaEye, FaEyeSlash } from 'react-icons/fa';
import { loginUser, getCurrentUser } from '../services';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = ({ onLogin }) => {
  const [loginData, setLoginData] = useState({ username: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const toast = useToast();
  const navigate = useNavigate();
  const { login: authLogin } = useAuth();

  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  const handleLoginChange = (e) => {
    const { name, value } = e.target;
    setLoginData({ ...loginData, [name]: value });
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      if (loginData.username && loginData.password) {
        try {
          const response = await loginUser(loginData);
          
          // Obtener los datos del usuario después de la autenticación
          try {
            const user = await getCurrentUser();
            
            // Store user data
            // Usar el nombre completo del usuario (name) obtenido de la API
            authLogin(response.access_token, user.name);
          } catch (error) {
            console.error('Error al obtener los datos del usuario:', error);
            // Si falla, seguir adelante con la autenticación sin un nombre específico
            authLogin(response.access_token);
          }
          
          toast({
            title: "Inicio de sesión exitoso",
            description: "Bienvenido a TZU Security",
            status: "success",
            duration: 3000,
            isClosable: true,
          });
          
          // Llamar a onLogin si existe
          if (onLogin) {
            onLogin(true);
          }
          
          // Redireccionar después de un pequeño delay para que se muestre el toast
          setTimeout(() => {
            navigate('/');
          }, 1000);
        } catch (err) {
          setError('Usuario o contraseña incorrectos');
        }
      } else {
        setError('Por favor, completa todos los campos');
      }
    } catch (err) {
      setError('Error de conexión. Intenta de nuevo.');
    } finally {
      setIsLoading(false);
    }
  };
  
  // Se eliminó la función handleRegisterSubmit ya que no necesitamos la funcionalidad de registro

  return (
    <Flex
      minH="100vh"
      align="center"
      justify="center"
      bgGradient="linear(to-b, blue.800, blue.900)" // Gradiente azul oscuro profesional para ciberseguridad
      position="relative"
      px={4}
      _before={{
        content: '""',
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        bgImage: "radial-gradient(circle at 25px 25px, rgba(255, 255, 255, 0.05) 2%, transparent 0%), linear-gradient(135deg, rgba(66, 153, 225, 0.1) 0%, rgba(0, 0, 0, 0) 50%)",
        backgroundSize: "30px 30px, cover",
        opacity: 0.6, // Efecto sutil de textura digital
      }}
    >
      <Card
        maxW="500px"
        w="full"
        bg={cardBg}
        borderColor="rgba(66, 153, 225, 0.3)" // Borde sutil con color azul
        borderWidth="1px"
        borderRadius="xl"
        shadow="2xl"
        overflow="hidden"
        _hover={{ boxShadow: "0 0 20px rgba(66, 153, 225, 0.2)" }} // Sutil resplandor al pasar el cursor
        transition="box-shadow 0.3s ease"
      >
        <CardBody p={8}>
          <VStack spacing={6} align="center">
            {/* Logo y título */}
            <VStack spacing={4}>
              <Image
                src="/tzu.png"
                alt="Tzu Logo"
                boxSize="100px"
                objectFit="contain"
                filter="drop-shadow(0px 4px 6px rgba(0, 0, 0, 0.2))"
              />
              <VStack spacing={1}>
                <Heading
                  size="lg"
                  color="blue.600"
                  textAlign="center"
                  fontWeight="bold"
                  letterSpacing="tight"
                >
                  TZU Security
                </Heading>
                <Text
                  fontSize="sm"
                  color="gray.600"
                  textAlign="center"
                  fontWeight="medium"
                  letterSpacing="wider"
                >
                 Threat Zero Utility
                </Text>
              </VStack>
            </VStack>

            {/* Formulario de inicio de sesión */}
            <Box w="full">
              <form onSubmit={handleLoginSubmit}>
                <VStack spacing={4}>
                  {error && (
                    <Alert status="error" borderRadius="md">
                      <AlertIcon />
                      {error}
                    </Alert>
                  )}

                  <FormControl isRequired>
                    <FormLabel fontSize="sm" color="gray.600">
                      Usuario
                    </FormLabel>
                    <InputGroup>
                      <InputLeftElement pointerEvents="none">
                        <FaUser color="gray" />
                      </InputLeftElement>
                      <Input
                        type="text"
                        name="username"
                        value={loginData.username}
                        onChange={handleLoginChange}
                        placeholder="Ingresa tu usuario"
                        borderColor={borderColor}
                        _hover={{ borderColor: 'blue.400' }}
                        _focus={{ borderColor: 'blue.500', boxShadow: '0 0 0 1px blue.500' }}
                        bg="gray.50"
                      />
                    </InputGroup>
                  </FormControl>

                  <FormControl isRequired>
                    <FormLabel fontSize="sm" color="gray.600">
                      Contraseña
                    </FormLabel>
                    <InputGroup>
                      <InputLeftElement pointerEvents="none">
                        <FaLock color="gray" />
                      </InputLeftElement>
                      <Input
                        type={showPassword ? 'text' : 'password'}
                        name="password"
                        value={loginData.password}
                        onChange={handleLoginChange}
                        placeholder="Ingresa tu contraseña"
                        borderColor={borderColor}
                        _hover={{ borderColor: 'blue.400' }}
                        _focus={{ borderColor: 'blue.500', boxShadow: '0 0 0 1px blue.500' }}
                        bg="gray.50"
                      />
                      <InputRightElement>
                        <IconButton
                          variant="ghost"
                          size="sm"
                          onClick={() => setShowPassword(!showPassword)}
                          icon={showPassword ? <FaEyeSlash /> : <FaEye />}
                          aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
                        />
                      </InputRightElement>
                    </InputGroup>
                  </FormControl>

                  <Button
                    type="submit"
                    bgGradient="linear(to-r, blue.500, blue.700)"
                    _hover={{ 
                      bgGradient: "linear(to-r, blue.600, blue.800)",
                      transform: "translateY(-2px)",
                      boxShadow: "lg"
                    }}
                    size="lg"
                    w="full"
                    mt={4}
                    isLoading={isLoading}
                    loadingText="Iniciando sesión..."
                    boxShadow="md"
                    color="white"
                    transition="all 0.3s"
                    fontWeight="medium"
                    letterSpacing="wide"
                  >
                    Iniciar Sesión
                  </Button>
                </VStack>
              </form>
            </Box>
          </VStack>
        </CardBody>
      </Card>
    </Flex>
  );
};

export default Login;
