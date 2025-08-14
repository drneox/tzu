import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {getInformationSystems} from "../services";
import { 
  Flex, 
  TableContainer, 
  Table, 
  Tr, 
  Td, 
  Thead, 
  Th, 
  Tbody,
  Button,
  HStack,
  Text,
  Box,
  Select,
  Spinner
} from "@chakra-ui/react";
import { ChevronLeftIcon, ChevronRightIcon } from '@chakra-ui/icons';
import { useLocalization } from '../hooks/useLocalization';

const Index = () => {
  const { t } = useLocalization();
  const [isLoading, setIsLoading] = useState(true);
  const [serviceData, setServiceData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalSystems, setTotalSystems] = useState(0);
  const [pageSize, setPageSize] = useState(10);
  const [totalPages, setTotalPages] = useState(1);

  const fetchData = async (page, size) => {
    setIsLoading(true);
    try {
      const skip = (page - 1) * size;
      const res = await getInformationSystems(skip, size);
      setServiceData(res.data);
      
      // Actualizamos el total de sistemas usando el contador real de la API
      if (res.totalCount !== undefined) {
        setTotalSystems(res.totalCount);
        console.log(`Total de sistemas obtenido de la API: ${res.totalCount}`);
      }
      // Como respaldo, estimamos el total basado en los datos recibidos
      else if (res.data.length > 0) {
        // Si estamos en la última página y hay menos registros que el tamaño de página
        if (page > 1 && res.data.length < size) {
          const newTotal = (page - 1) * size + res.data.length;
          setTotalSystems(newTotal);
          console.log(`Estimando total de sistemas: ${newTotal} (página incompleta)`);
        } else if (page === 1 && res.data.length < size) {
          setTotalSystems(res.data.length);
          console.log(`Estimando total de sistemas: ${res.data.length} (primera página)`);
        } else {
          // En caso contrario, aumentamos el contador en cada llamada
          const newTotal = Math.max(totalSystems, page * size + 1); // +1 para asegurar que haya otra página
          setTotalSystems(newTotal);
          console.log(`Estimando total de sistemas: ${newTotal} (página completa)`);
        }
      } else {
        // Si no hay datos, el total es 0
        setTotalSystems(0);
        console.log('No hay sistemas disponibles');
      }
      
    } catch (error) {
      console.error("Error al cargar los sistemas:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Calculamos el número total de páginas cuando cambia totalSystems o pageSize
  useEffect(() => {
    const calculatedPages = Math.max(1, Math.ceil(totalSystems / pageSize));
    setTotalPages(calculatedPages);
    console.log(`Recalculando totalPages: ${calculatedPages} (totalSystems: ${totalSystems}, pageSize: ${pageSize})`);
  }, [totalSystems, pageSize]);

  // Cargamos datos iniciales y cuando cambia la paginación
  useEffect(() => {
    fetchData(currentPage, pageSize);
  }, [currentPage, pageSize]);

  const handlePageChange = (newPage) => {
    // Asegurarse de que la página esté en el rango válido
    if (newPage >= 1 && newPage <= totalPages) {
      console.log(`Cambiando a página ${newPage} de ${totalPages}`);
      setCurrentPage(newPage);
    } else {
      console.log(`Intento de cambiar a página inválida: ${newPage} (totalPages: ${totalPages})`);
    }
  };

  const handlePageSizeChange = (event) => {
    const newSize = parseInt(event.target.value);
    setPageSize(newSize);
    setCurrentPage(1); // Volver a la primera página al cambiar el tamaño
  };

  if (isLoading && serviceData.length === 0) {
    return (
      <Flex align="center" justify="center" height="50vh">
        <Spinner size="xl" color="blue.500" thickness="4px" />
        <Text ml={4} fontSize="xl">{t?.ui?.loading || 'Cargando...'}</Text>
      </Flex>
    );
  }

  return (
    <Flex
      direction="column"
      align="center"
      padding="0.5rem"
      justify="center"
      style={{ marginBottom: "60px" }}
    >
      <Box width="100%" maxWidth="1000px">
        <TableContainer>
          <Table border="2px solid gray" borderCollapse="collapse" variant='striped' colorScheme='gray' overflowX='auto' whiteSpace='normal' width="100%">
            <Thead>
              <Tr bg="blue.500" color="white" p="4">
                <Th color="white" p="3" shadow="md">{t?.ui?.table?.title || 'Título'}</Th>
                <Th color="white" p="3" shadow="md">{t?.ui?.table?.description || 'Descripción'}</Th>
                <Th color="white" p="3" shadow="md" maxWidth='180px'>{t?.ui?.table?.date || 'Fecha'}</Th>
              </Tr>
            </Thead>
            <Tbody>
              {serviceData.length === 0 ? (
                <Tr>
                  <Td colSpan={3} textAlign="center" py={6}>
                    {t?.ui?.no_systems || 'No hay sistemas disponibles'}
                  </Td>
                </Tr>
              ) : (
                serviceData.map(data => {
                  const dateTime = new Date(data.datetime).toLocaleString();
                  return (
                    <Tr key={data.id}>
                      <Td><Link to={`analysis/${data.id}`} style={{ color: 'blue.600', fontWeight: 'medium' }}>{String(data.title)}</Link></Td>
                      <Td>{data.description}</Td>
                      <Td>{dateTime}</Td>
                    </Tr>
                  );
                })
              )}
              {isLoading && (
                <Tr>
                  <Td colSpan={3} textAlign="center" py={4}>
                    <Spinner size="sm" color="blue.500" mr={2} />
                    {t?.ui?.loading_more || 'Cargando más resultados...'}
                  </Td>
                </Tr>
              )}
            </Tbody>
          </Table>
        </TableContainer>

        {/* Paginador */}
        <Flex justify="space-between" align="center" mt={4} px={2}>
          <HStack spacing={2}>
            <Text fontSize="sm">{t?.ui?.rows_per_page || 'Filas por página'}:</Text>
            <Select 
              value={pageSize} 
              onChange={handlePageSizeChange}
              size="sm"
              width="70px"
            >
              <option value={5}>5</option>
              <option value={10}>10</option>
              <option value={20}>20</option>
              <option value={50}>50</option>
            </Select>
          </HStack>
          
          <HStack spacing={2}>
            <Text fontSize="sm">
              {(currentPage - 1) * pageSize + 1}-{Math.min(currentPage * pageSize, totalSystems)} {t?.ui?.of || 'de'} {totalSystems}
            </Text>
            
            <Button
              size="sm"
              onClick={() => handlePageChange(currentPage - 1)}
              isDisabled={currentPage === 1}
              leftIcon={<ChevronLeftIcon />}
              variant="outline"
            >
              {t?.ui?.previous || 'Anterior'}
            </Button>
            
            <Text fontSize="sm">
              {t?.ui?.page || 'Página'} {currentPage} {t?.ui?.of || 'de'} {totalPages}
            </Text>
            
            <Button
              size="sm"
              onClick={() => handlePageChange(currentPage + 1)}
              isDisabled={currentPage >= totalPages}
              rightIcon={<ChevronRightIcon />}
              variant="outline"
            >
              {t?.ui?.next || 'Siguiente'}
            </Button>
          </HStack>
        </Flex>
      </Box>
    </Flex>
  );
};

export default Index;