import React, { useState, useEffect } from 'react';
import {
  Box, Button, Table, Thead, Tbody, Tr, Th, Td,
  Select, Badge, Heading, HStack, VStack, useToast,
  Modal, ModalOverlay, ModalContent, ModalHeader,
  ModalBody, ModalFooter, ModalCloseButton,
  FormControl, FormLabel, Input, useDisclosure,
  Spinner, Tabs, TabList, Tab, TabPanels, TabPanel, Text
} from '@chakra-ui/react';
import { getUsers, createUser, updateUserRole, updateUserActive, deleteUser, getAuditLog } from '../services/apiClient';
import { useLocalization } from '../hooks/useLocalization';

const ROLES = ['admin', 'analyst', 'reader'];

const UserManagement = () => {
  const { t } = useLocalization();
  const tU = t?.ui?.users || {};
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [newUser, setNewUser] = useState({ username: '', email: '', name: '', password: '', role: 'reader' });
  const [auditLog, setAuditLog] = useState([]);
  const [auditLoading, setAuditLoading] = useState(false);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const toast = useToast();

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const data = await getUsers();
      setUsers(data);
    } catch (err) {
      toast({ title: tU.error_loading || 'Error loading users', description: err.message, status: 'error', duration: 4000 });
    } finally {
      setLoading(false);
    }
  };

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { fetchUsers(); }, []);

  const fetchAuditLog = async () => {
    setAuditLoading(true);
    try {
      const data = await getAuditLog({ limit: 100 });
      setAuditLog(data);
    } catch (err) {
      toast({ title: 'Error loading audit log', description: err.message, status: 'error', duration: 4000 });
    } finally {
      setAuditLoading(false);
    }
  };

  const handleCreate = async () => {
    setSubmitting(true);
    try {
      await createUser(newUser);
      toast({ title: tU.created || 'User created', status: 'success', duration: 3000 });
      setNewUser({ username: '', email: '', name: '', password: '', role: 'reader' });
      onClose();
      fetchUsers();
    } catch (err) {
      toast({ title: tU.error_creating || 'Error creating user', description: err.response?.data?.detail || err.message, status: 'error', duration: 4000 });
    } finally {
      setSubmitting(false);
    }
  };

  const handleRoleChange = async (userId, role) => {
    try {
      await updateUserRole(userId, role);
      toast({ title: tU.role_updated || 'Role updated', status: 'success', duration: 2000 });
      fetchUsers();
    } catch (err) {
      toast({ title: tU.error_role || 'Error updating role', description: err.response?.data?.detail || err.message, status: 'error', duration: 4000 });
    }
  };

  const handleToggleActive = async (userId, currentActive) => {
    try {
      await updateUserActive(userId, !currentActive);
      const label = !currentActive ? (tU.activated || 'activated') : (tU.deactivated || 'deactivated');
      toast({ title: `${tU.status_changed || 'Status'}: ${label}`, status: 'success', duration: 2000 });
      fetchUsers();
    } catch (err) {
      toast({ title: tU.error_status || 'Error changing status', description: err.response?.data?.detail || err.message, status: 'error', duration: 4000 });
    }
  };

  const handleDelete = async (userId, username) => {
    if (!window.confirm(`${tU.confirm_delete || 'Delete user?'} "${username}"`)) return;
    try {
      await deleteUser(userId);
      toast({ title: tU.deleted || 'User deleted', status: 'success', duration: 2000 });
      fetchUsers();
    } catch (err) {
      toast({ title: tU.error_deleting || 'Error deleting user', description: err.response?.data?.detail || err.message, status: 'error', duration: 4000 });
    }
  };

  if (loading) return <Spinner mt={8} />;

  return (
    <Box p={6}>
      <HStack justify="space-between" mb={6}>
        <Heading size="lg">{tU.title || 'User Management'}</Heading>
        <Button colorScheme="indigo" onClick={onOpen}>{tU.new_user || '+ New User'}</Button>
      </HStack>

      <Tabs onChange={(idx) => { if (idx === 1) fetchAuditLog(); }}>
        <TabList>
          <Tab>{tU.users_tab || 'Users'}</Tab>
          <Tab>{tU.audit_tab || 'Audit Log'}</Tab>
        </TabList>
        <TabPanels>
          <TabPanel px={0}>
      <Table variant="simple" size="sm">
        <Thead>
          <Tr>
            <Th>{tU.username || 'Username'}</Th>
            <Th>{tU.email || 'Email'}</Th>
            <Th>{tU.name || 'Name'}</Th>
            <Th>{tU.role || 'Role'}</Th>
            <Th>{tU.status || 'Status'}</Th>
            <Th>{tU.actions || 'Actions'}</Th>
          </Tr>
        </Thead>
        <Tbody>
          {users.map((usr) => (
            <Tr key={usr.id}>
              <Td fontWeight="medium">{usr.username}</Td>
              <Td>{usr.email}</Td>
              <Td>{usr.name}</Td>
              <Td>
                <Select
                  size="xs"
                  value={usr.role}
                  onChange={(e) => handleRoleChange(usr.id, e.target.value)}
                  width="110px"
                >
                  {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
                </Select>
              </Td>
              <Td>
                <Badge colorScheme={usr.is_active ? 'green' : 'red'}>
                  {usr.is_active ? (tU.active || 'Active') : (tU.inactive || 'Inactive')}
                </Badge>
              </Td>
              <Td>
                <HStack spacing={2}>
                  <Button size="xs" onClick={() => handleToggleActive(usr.id, usr.is_active)}>
                    {usr.is_active ? (tU.deactivate || 'Deactivate') : (tU.activate || 'Activate')}
                  </Button>
                  <Button size="xs" colorScheme="red" variant="outline" onClick={() => handleDelete(usr.id, usr.username)}>
                    {tU.delete || 'Delete'}
                  </Button>
                </HStack>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
          </TabPanel>
          <TabPanel px={0}>
            {auditLoading ? <Spinner /> : (
              <Table variant="simple" size="sm">
                <Thead>
                  <Tr>
                    <Th>Timestamp</Th>
                    <Th>Action</Th>
                    <Th>Performed By</Th>
                    <Th>Target User</Th>
                    <Th>Detail</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {auditLog.length === 0 && (
                    <Tr><Td colSpan={5}><Text color="gray.500">No audit log entries</Text></Td></Tr>
                  )}
                  {auditLog.map((entry) => (
                    <Tr key={entry.id}>
                      <Td fontSize="xs">{new Date(entry.timestamp).toLocaleString()}</Td>
                      <Td><Badge>{entry.action}</Badge></Td>
                      <Td fontSize="xs">{entry.performed_by_id}</Td>
                      <Td fontSize="xs">{entry.target_user_id || '-'}</Td>
                      <Td fontSize="xs">{entry.detail || '-'}</Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            )}
          </TabPanel>
        </TabPanels>
      </Tabs>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{tU.create_title || 'Create New User'}</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack spacing={3}>
              <FormControl isRequired>
                <FormLabel>{tU.username || 'Username'}</FormLabel>
                <Input value={newUser.username} onChange={(e) => setNewUser({ ...newUser, username: e.target.value })} />
              </FormControl>
              <FormControl isRequired>
                <FormLabel>{tU.email || 'Email'}</FormLabel>
                <Input type="email" value={newUser.email} onChange={(e) => setNewUser({ ...newUser, email: e.target.value })} />
              </FormControl>
              <FormControl isRequired>
                <FormLabel>{tU.full_name || 'Full Name'}</FormLabel>
                <Input value={newUser.name} onChange={(e) => setNewUser({ ...newUser, name: e.target.value })} />
              </FormControl>
              <FormControl isRequired>
                <FormLabel>{tU.password || 'Password'}</FormLabel>
                <Input type="password" value={newUser.password} onChange={(e) => setNewUser({ ...newUser, password: e.target.value })} />
              </FormControl>
              <FormControl>
                <FormLabel>{tU.role || 'Role'}</FormLabel>
                <Select value={newUser.role} onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}>
                  {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
                </Select>
              </FormControl>
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onClose}>{tU.cancel || 'Cancel'}</Button>
            <Button colorScheme="indigo" onClick={handleCreate} isLoading={submitting}>{tU.create || 'Create'}</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default UserManagement;
