import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {getInformationSystems} from "../services";
import { archiveInformationSystem } from "../services/informationSystemService";
import { getProjects } from "../services/projectService";
import { useAuth } from "../context/AuthContext";
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
  Spinner,
  Badge,
  Switch,
  FormLabel,
  useToast,
  Tooltip,
  IconButton,
} from "@chakra-ui/react";
import { ChevronLeftIcon, ChevronRightIcon } from '@chakra-ui/icons';
import { MdArchive, MdUnarchive } from 'react-icons/md';
import { useLocalization } from '../hooks/useLocalization';

const Index = () => {
  const { t } = useLocalization();
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin';
  const toast = useToast();
  const [isLoading, setIsLoading] = useState(true);
  const [serviceData, setServiceData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalSystems, setTotalSystems] = useState(0);
  const [pageSize, setPageSize] = useState(10);
  const [totalPages, setTotalPages] = useState(1);
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState('');
  const [showArchived, setShowArchived] = useState(false);
  const [archivingId, setArchivingId] = useState(null);

  useEffect(() => {
    getProjects().then((res) => setProjects(res.data)).catch(() => {});
  }, []);

  const fetchData = async (page, size, projectId, includeArchived) => {
    setIsLoading(true);
    try {
      const skip = (page - 1) * size;
      const res = await getInformationSystems(skip, size, projectId || null, includeArchived);
      setServiceData(res.data);
      
      if (res.totalCount !== undefined) {
        setTotalSystems(res.totalCount);
      } else if (res.data.length > 0) {
        if (page > 1 && res.data.length < size) {
          setTotalSystems((page - 1) * size + res.data.length);
        } else if (page === 1 && res.data.length < size) {
          setTotalSystems(res.data.length);
        } else {
          setTotalSystems(Math.max(totalSystems, page * size + 1));
        }
      } else {
        setTotalSystems(0);
      }
    } catch (error) {
      console.error("Error al cargar los sistemas:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const calculatedPages = Math.max(1, Math.ceil(totalSystems / pageSize));
    setTotalPages(calculatedPages);
  }, [totalSystems, pageSize]);

  useEffect(() => {
    fetchData(currentPage, pageSize, selectedProjectId, showArchived);
  }, [currentPage, pageSize, selectedProjectId, showArchived]);

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
    }
  };

  const handlePageSizeChange = (event) => {
    setPageSize(parseInt(event.target.value));
    setCurrentPage(1);
  };

  const handleProjectFilterChange = (event) => {
    setSelectedProjectId(event.target.value);
    setCurrentPage(1);
  };

  const handleToggleArchive = async (id, currentArchived) => {
    setArchivingId(id);
    try {
      const result = await archiveInformationSystem(id);
      const newState = result.archived;
      toast({
        title: newState
          ? (t?.index?.archived_success || 'Evaluación archivada')
          : (t?.index?.unarchived_success || 'Evaluación desarchivada'),
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      // Refresh list
      fetchData(currentPage, pageSize, selectedProjectId, showArchived);
    } catch (err) {
      toast({
        title: t?.index?.archive_error || 'Error al cambiar estado de archivo',
        status: 'error',
        duration: 4000,
        isClosable: true,
      });
    } finally {
      setArchivingId(null);
    }
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
        {/* Project filter + archive toggle */}
        <Flex mb={3} align="center" gap={4} wrap="wrap">
          <Flex align="center" gap={2}>
            <Text fontSize="sm" fontWeight="medium" whiteSpace="nowrap">
              {t?.projects?.project || 'Proyecto'}:
            </Text>
            <Select
              value={selectedProjectId}
              onChange={handleProjectFilterChange}
              size="sm"
              maxWidth="260px"
            >
              <option value="">{t?.projects?.filterAll || 'Todos los proyectos'}</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </Select>
          </Flex>
          {isAdmin && (
            <Flex align="center" gap={2}>
              <FormLabel htmlFor="show-archived" mb="0" fontSize="sm" fontWeight="medium" whiteSpace="nowrap">
                {t?.index?.show_archived || 'Mostrar archivados'}
              </FormLabel>
              <Switch
                id="show-archived"
                isChecked={showArchived}
                onChange={(e) => { setShowArchived(e.target.checked); setCurrentPage(1); }}
                colorScheme="teal"
                size="sm"
              />
            </Flex>
          )}
        </Flex>

        <TableContainer>
          <Table border="2px solid gray" borderCollapse="collapse" variant='striped' colorScheme='gray' overflowX='auto' whiteSpace='normal' width="100%">
            <Thead>
              <Tr bg="blue.500" color="white" p="4">
                <Th color="white" p="3" shadow="md">{t?.ui?.table?.title || 'Título'}</Th>
                <Th color="white" p="3" shadow="md">{t?.ui?.table?.description || 'Descripción'}</Th>
                <Th color="white" p="3" shadow="md">{t?.projects?.project || 'Proyecto'}</Th>
                <Th color="white" p="3" shadow="md" maxWidth='180px'>{t?.ui?.table?.date || 'Fecha'}</Th>
                {isAdmin && <Th color="white" p="3" shadow="md">{t?.ui?.table?.actions || 'Acciones'}</Th>}
              </Tr>
            </Thead>
            <Tbody>
              {serviceData.length === 0 ? (
                <Tr>
                  <Td colSpan={isAdmin ? 5 : 4} textAlign="center" py={6}>
                    {t?.ui?.no_systems || 'No hay sistemas disponibles'}
                  </Td>
                </Tr>
              ) : (
                serviceData.map(data => {
                  const dateTime = new Date(data.datetime).toLocaleString();
                  return (
                    <Tr key={data.id} opacity={data.archived ? 0.6 : 1}>
                      <Td>
                        <Flex align="center" gap={2} wrap="wrap">
                          <Link to={`/analysis/${data.id}`} style={{ color: 'blue.600', fontWeight: 'medium' }}>{String(data.title)}</Link>
                          {data.archived && (
                            <Badge colorScheme="gray" borderRadius="md" px={2}>
                              {t?.index?.archived_badge || 'Archivado'}
                            </Badge>
                          )}
                        </Flex>
                      </Td>
                      <Td>{data.description}</Td>
                      <Td>
                        {data.project_name
                          ? <Badge colorScheme="blue" borderRadius="md" px={2}>{data.project_name}</Badge>
                          : <Text color="gray.400" fontSize="sm">{t?.projects?.noProject || '—'}</Text>
                        }
                      </Td>
                      <Td>{dateTime}</Td>
                      {isAdmin && (
                        <Td>
                          <Tooltip label={data.archived ? (t?.index?.unarchive || 'Desarchivar') : (t?.index?.archive || 'Archivar')}>
                            <IconButton
                              aria-label={data.archived ? (t?.index?.unarchive || 'Desarchivar') : (t?.index?.archive || 'Archivar')}
                              icon={data.archived ? <MdUnarchive size="16" /> : <MdArchive size="16" />}
                              size="xs"
                              variant="ghost"
                              colorScheme={data.archived ? 'teal' : 'gray'}
                              isLoading={archivingId === data.id}
                              onClick={() => handleToggleArchive(data.id, data.archived)}
                            />
                          </Tooltip>
                        </Td>
                      )}
                    </Tr>
                  );
                })
              )}
              {isLoading && (
                <Tr>
                  <Td colSpan={isAdmin ? 5 : 4} textAlign="center" py={4}>
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
