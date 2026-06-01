import { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Flex,
  Heading,
  IconButton,
  Input,
  Spinner,
  Table,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
  useToast,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
  useDisclosure,
  Badge,
  Textarea,
  HStack,
} from '@chakra-ui/react';
import { DeleteIcon, EditIcon, ChevronDownIcon, ChevronRightIcon } from '@chakra-ui/icons';
import { useRef } from 'react';
import {
  getProjects,
  createProject,
  updateProject,
  deleteProject,
} from '../services/projectService';
import { useLocalization } from '../hooks/useLocalization';
import { useAuth } from '../context/AuthContext';
import ProjectMembersManager from './ProjectMembersManager';

const ProjectManager = () => {
  const { t } = useLocalization();
  const { isAdmin, canWrite, user } = useAuth();
  const toast = useToast();

  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [expandedId, setExpandedId] = useState(null);

  // New project form
  const [newName, setNewName] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [isCreating, setIsCreating] = useState(false);

  // Edit state
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState('');
  const [editDesc, setEditDesc] = useState('');

  // Delete confirmation
  const { isOpen: isDeleteOpen, onOpen: onDeleteOpen, onClose: onDeleteClose } = useDisclosure();
  const [deletingProject, setDeletingProject] = useState(null);
  const cancelRef = useRef();

  const loadProjects = async () => {
    setIsLoading(true);
    try {
      const res = await getProjects();
      setProjects(res.data);
    } catch {
      toast({ title: 'Error', description: 'No se pudo cargar los proyectos', status: 'error', duration: 3000 });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { loadProjects(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newName.trim()) return;
    setIsCreating(true);
    try {
      await createProject({ name: newName.trim(), description: newDesc.trim() || null });
      setNewName('');
      setNewDesc('');
      toast({ title: t?.projects?.created || 'Proyecto creado', status: 'success', duration: 2000 });
      loadProjects();
    } catch (err) {
      toast({ title: 'Error', description: err?.response?.data?.detail || 'No se pudo crear', status: 'error', duration: 3000 });
    } finally {
      setIsCreating(false);
    }
  };

  const startEdit = (p) => {
    setEditingId(p.id);
    setEditName(p.name);
    setEditDesc(p.description || '');
  };

  const handleUpdate = async (projectId) => {
    try {
      await updateProject(projectId, { name: editName.trim(), description: editDesc.trim() || null });
      setEditingId(null);
      toast({ title: t?.projects?.updated || 'Proyecto actualizado', status: 'success', duration: 2000 });
      loadProjects();
    } catch (err) {
      toast({ title: 'Error', description: err?.response?.data?.detail || 'No se pudo actualizar', status: 'error', duration: 3000 });
    }
  };

  const confirmDelete = (p) => {
    setDeletingProject(p);
    onDeleteOpen();
  };

  const handleDelete = async () => {
    if (!deletingProject) return;
    try {
      await deleteProject(deletingProject.id);
      toast({ title: t?.projects?.deleted || 'Proyecto eliminado', status: 'info', duration: 2000 });
      onDeleteClose();
      loadProjects();
    } catch (err) {
      toast({ title: 'Error', description: err?.response?.data?.detail || 'No se pudo eliminar', status: 'error', duration: 3000 });
    }
  };

  const canManage = (project) =>
    isAdmin || (user && String(project.created_by) === String(user.id));

  if (isLoading) {
    return (
      <Flex align="center" justify="center" mt={10}>
        <Spinner size="xl" color="blue.500" />
      </Flex>
    );
  }

  return (
    <Box maxWidth="900px" mx="auto" mt={6} px={4}>
      <Heading size="md" mb={4}>{t?.projects?.title || 'Proyectos'}</Heading>

      {/* Create form */}
      {canWrite && (
        <Box as="form" onSubmit={handleCreate} mb={6} p={4} borderWidth={1} borderRadius={8} bg="gray.50">
          <Heading size="sm" mb={3}>{t?.projects?.created ? 'Nuevo proyecto' : 'New project'}</Heading>
          <HStack mb={2}>
            <Input
              placeholder={t?.projects?.namePlaceholder || 'Nombre del proyecto'}
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              required
              size="sm"
            />
          </HStack>
          <Textarea
            placeholder={t?.projects?.description || 'Descripción (opcional)'}
            value={newDesc}
            onChange={(e) => setNewDesc(e.target.value)}
            size="sm"
            mb={2}
            rows={2}
          />
          <Button type="submit" colorScheme="teal" size="sm" isLoading={isCreating}>
            {t?.projects?.created || 'Crear proyecto'}
          </Button>
        </Box>
      )}

      {/* Projects table */}
      {projects.length === 0 ? (
        <Text color="gray.500">{t?.projects?.noProject || 'No hay proyectos'}</Text>
      ) : (
        <Table variant="simple" size="sm">
          <Thead bg="blue.500">
            <Tr>
              <Th color="white" w="8"></Th>
              <Th color="white">{t?.projects?.title || 'Proyecto'}</Th>
              <Th color="white">{t?.projects?.description || 'Descripción'}</Th>
              <Th color="white" isNumeric>{t?.projects?.analyses || 'Análisis'}</Th>
              <Th color="white" isNumeric>{t?.projects?.members || 'Miembros'}</Th>
              <Th color="white" w="28"></Th>
            </Tr>
          </Thead>
          <Tbody>
            {projects.map((p) => (
              <>
                <Tr key={p.id} _hover={{ bg: 'gray.50' }}>
                  <Td>
                    <IconButton
                      icon={expandedId === p.id ? <ChevronDownIcon /> : <ChevronRightIcon />}
                      size="xs"
                      variant="ghost"
                      aria-label="toggle members"
                      onClick={() => setExpandedId(expandedId === p.id ? null : p.id)}
                    />
                  </Td>
                  <Td>
                    {editingId === p.id ? (
                      <Input
                        size="xs"
                        value={editName}
                        onChange={(e) => setEditName(e.target.value)}
                        autoFocus
                      />
                    ) : (
                      <Text fontWeight="medium">{p.name}</Text>
                    )}
                  </Td>
                  <Td>
                    {editingId === p.id ? (
                      <Input
                        size="xs"
                        value={editDesc}
                        onChange={(e) => setEditDesc(e.target.value)}
                      />
                    ) : (
                      <Text color="gray.600" fontSize="sm" noOfLines={1}>{p.description || '—'}</Text>
                    )}
                  </Td>
                  <Td isNumeric>
                    <Badge colorScheme="blue">{p.analysis_count}</Badge>
                  </Td>
                  <Td isNumeric>
                    <Badge colorScheme="green">{p.member_count}</Badge>
                  </Td>
                  <Td>
                    {canManage(p) && (
                      <HStack spacing={1} justify="flex-end">
                        {editingId === p.id ? (
                          <>
                            <Button size="xs" colorScheme="teal" onClick={() => handleUpdate(p.id)}>✓</Button>
                            <Button size="xs" onClick={() => setEditingId(null)}>✕</Button>
                          </>
                        ) : (
                          <>
                            <IconButton
                              icon={<EditIcon />}
                              size="xs"
                              variant="ghost"
                              colorScheme="blue"
                              aria-label="edit"
                              onClick={() => startEdit(p)}
                            />
                            <IconButton
                              icon={<DeleteIcon />}
                              size="xs"
                              variant="ghost"
                              colorScheme="red"
                              aria-label="delete"
                              onClick={() => confirmDelete(p)}
                            />
                          </>
                        )}
                      </HStack>
                    )}
                  </Td>
                </Tr>
                {expandedId === p.id && (
                  <Tr key={`members-${p.id}`}>
                    <Td colSpan={6} bg="gray.50" p={4}>
                      <ProjectMembersManager project={p} canManage={canManage(p)} />
                    </Td>
                  </Tr>
                )}
              </>
            ))}
          </Tbody>
        </Table>
      )}

      {/* Delete confirmation dialog */}
      <AlertDialog isOpen={isDeleteOpen} leastDestructiveRef={cancelRef} onClose={onDeleteClose}>
        <AlertDialogOverlay>
          <AlertDialogContent>
            <AlertDialogHeader>{t?.projects?.deleteConfirm || '¿Eliminar proyecto?'}</AlertDialogHeader>
            <AlertDialogBody>
              <Text><strong>{deletingProject?.name}</strong></Text>
              <Text mt={2} fontSize="sm" color="gray.600">
                Las análisis asignadas a este proyecto quedarán sin proyecto asignado.
              </Text>
            </AlertDialogBody>
            <AlertDialogFooter>
              <Button ref={cancelRef} onClick={onDeleteClose}>Cancelar</Button>
              <Button colorScheme="red" onClick={handleDelete} ml={3}>Eliminar</Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
    </Box>
  );
};

export default ProjectManager;
