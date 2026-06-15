import React, { useState } from 'react';
import {
  Box,
  VStack,
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
import { colors } from '../theme/colors';
import Logo from './Logo';

const Login = ({ onLogin }) => {
  const [loginData, setLoginData] = useState({ username: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const toast = useToast();
  const navigate = useNavigate();
  const { login: authLogin } = useAuth();

  const bgColor = useColorModeValue('slate.50', 'slate.900');
  const cardBg = useColorModeValue('white', 'slate.800');
  const borderColor = useColorModeValue('slate.200', 'slate.600');

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
      bg={bgColor}
      position="relative"
      px={4}
    >
      <Card
        maxW="420px"
        w="full"
        bg={cardBg}
        borderColor={borderColor}
        borderWidth="1px"
        borderRadius="xl"
        shadow="lg"
        overflow="hidden"
      >
        <CardBody p={8}>
          <VStack spacing={6} align="center">
            {/* Logo y título */}
            <VStack spacing={4}>
              <Logo size="56px" p="8px" />
              <VStack spacing={1}>
                <Heading
                  size="lg"
                  color="slate.800"
                  textAlign="center"
                  fontWeight="bold"
                  letterSpacing="tight"
                >
                  TZU Login
                </Heading>
                <Text
                  fontSize="sm"
                  color="slate.500"
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
                    <FormLabel fontSize="sm" color="slate.600">
                      Usuario
                    </FormLabel>
                    <InputGroup>
                      <InputLeftElement pointerEvents="none">
                        <FaUser color={colors.text.muted} />
                      </InputLeftElement>
                      <Input
                        type="text"
                        name="username"
                        value={loginData.username}
                        onChange={handleLoginChange}
                        placeholder="Ingresa tu usuario"
                        borderColor={borderColor}
                        _hover={{ borderColor: 'slate.300' }}
                        _focus={{ borderColor: 'indigo.500', boxShadow: `0 0 0 1px ${colors.primary.default}` }}
                        bg="slate.50"
                      />
                    </InputGroup>
                  </FormControl>

                  <FormControl isRequired>
                    <FormLabel fontSize="sm" color="slate.600">
                      Contraseña
                    </FormLabel>
                    <InputGroup>
                      <InputLeftElement pointerEvents="none">
                        <FaLock color={colors.text.muted} />
                      </InputLeftElement>
                      <Input
                        type={showPassword ? 'text' : 'password'}
                        name="password"
                        value={loginData.password}
                        onChange={handleLoginChange}
                        placeholder="Ingresa tu contraseña"
                        borderColor={borderColor}
                        _hover={{ borderColor: 'slate.300' }}
                        _focus={{ borderColor: 'indigo.500', boxShadow: `0 0 0 1px ${colors.primary.default}` }}
                        bg="slate.50"
                      />
                      <InputRightElement>
                        <IconButton
                          variant="ghost"
                          size="sm"
                          onClick={() => setShowPassword(!showPassword)}
                          icon={showPassword ? <FaEyeSlash /> : <FaEye />}
                          aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
                          color="slate.500"
                        />
                      </InputRightElement>
                    </InputGroup>
                  </FormControl>

                  <Button
                    type="submit"
                    bgGradient="linear(to-r, indigo.500, indigo.700)"
                    _hover={{
                      bgGradient: "linear(to-r, indigo.600, indigo.800)",
                      transform: "translateY(-1px)",
                      boxShadow: "md"
                    }}
                    _active={{ bgGradient: "linear(to-r, indigo.700, indigo.900)" }}
                    size="lg"
                    w="full"
                    mt={4}
                    isLoading={isLoading}
                    loadingText="Iniciando sesión..."
                    boxShadow="sm"
                    color="white"
                    transition="all 0.2s"
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
