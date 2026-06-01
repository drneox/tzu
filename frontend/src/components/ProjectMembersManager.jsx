import { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Flex,
  HStack,
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
  Badge,
} from '@chakra-ui/react';
import { DeleteIcon } from '@chakra-ui/icons';
import { getProjectMembers, addProjectMember, removeProjectMember } from '../services/projectService';
import { useLocalization } from '../hooks/useLocalization';

const ProjectMembersManager = ({ project, canManage }) => {
  const { t } = useLocalization();
  const toast = useToast();

  const [members, setMembers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [newUserId, setNewUserId] = useState('');
  const [isAdding, setIsAdding] = useState(false);

  const load = async () => {
    setIsLoading(true);
    try {
      const res = await getProjectMembers(project.id);
      setMembers(res.data);
    } catch {
      setMembers([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { load(); }, [project.id]);

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!newUserId.trim()) return;
    setIsAdding(true);
    try {
      await addProjectMember(project.id, { user_id: newUserId.trim() });
      setNewUserId('');
      toast({ title: t?.projects?.addMember || 'Miembro agregado', status: 'success', duration: 2000 });
      load();
    } catch (err) {
      toast({
        title: 'Error',
        description: err?.response?.data?.detail || 'No se pudo agregar el miembro',
        status: 'error',
        duration: 3000,
      });
    } finally {
      setIsAdding(false);
    }
  };

  const handleRemove = async (userId) => {
    try {
      await removeProjectMember(project.id, userId);
      toast({ title: t?.projects?.removeMember || 'Miembro eliminado', status: 'info', duration: 2000 });
      load();
    } catch (err) {
      toast({
        title: 'Error',
        description: err?.response?.data?.detail || 'No se pudo eliminar',
        status: 'error',
        duration: 3000,
      });
    }
  };

  if (isLoading) {
    return (
      <Flex align="center" gap={2}>
        <Spinner size="sm" />
        <Text fontSize="sm">Cargando miembros...</Text>
      </Flex>
    );
  }

  return (
    <Box>
      <Text fontWeight="semibold" mb={2} fontSize="sm">{t?.projects?.members || 'Miembros'}</Text>

      {members.length === 0 ? (
        <Text fontSize="sm" color="gray.500" mb={3}>No hay miembros asignados</Text>
      ) : (
        <Table size="xs" variant="simple" mb={3}>
          <Thead>
            <Tr>
              <Th fontSize="xs">Usuario</Th>
              <Th fontSize="xs">Nombre</Th>
              <Th fontSize="xs">Rol</Th>
              <Th fontSize="xs">Agregado</Th>
              {canManage && <Th w="10"></Th>}
            </Tr>
          </Thead>
          <Tbody>
            {members.map((m) => (
              <Tr key={m.user_id}>
                <Td fontSize="xs">{m.username}</Td>
                <Td fontSize="xs">{m.name}</Td>
                <Td fontSize="xs">
                  <Badge colorScheme={m.role === 'admin' ? 'red' : 'blue'} fontSize="2xs">{m.role}</Badge>
                </Td>
                <Td fontSize="xs">{new Date(m.added_at).toLocaleDateString()}</Td>
                {canManage && (
                  <Td>
                    <IconButton
                      icon={<DeleteIcon />}
                      size="xs"
                      variant="ghost"
                      colorScheme="red"
                      aria-label="remove"
                      onClick={() => handleRemove(m.user_id)}
                    />
                  </Td>
                )}
              </Tr>
            ))}
          </Tbody>
        </Table>
      )}

      {canManage && (
        <HStack as="form" onSubmit={handleAdd} spacing={2}>
          <Input
            placeholder="UUID del usuario..."
            value={newUserId}
            onChange={(e) => setNewUserId(e.target.value)}
            size="xs"
            maxWidth="280px"
          />
          <Button type="submit" size="xs" colorScheme="teal" isLoading={isAdding}>
            {t?.projects?.addMember || 'Agregar'}
          </Button>
        </HStack>
      )}
    </Box>
  );
};

export default ProjectMembersManager;
