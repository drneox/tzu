import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Flex, Box, Input, Button, Textarea, Heading, useToast, Alert, AlertIcon, FormLabel } from "@chakra-ui/react";
import { createInformationSystem } from "../services";
import { useLocalization } from '../hooks/useLocalization';
import { useAuth } from '../context/AuthContext';
import ProjectCombobox from './ProjectCombobox';

const CreateInformationSystem = () => {
  const { t } = useLocalization();
  const { canWrite } = useAuth();
  const toast = useToast();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [project, setProject] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = { title, description };
      if (project) {
        if (project.isNew) {
          data.project_name = project.name;
        } else {
          data.project_id = project.id;
        }
      }
      const res = await createInformationSystem(data);
      const id = res.data.id;
      
      toast({
        title: t?.ui?.form?.success_creating_title || "Success!",
        description: t?.ui?.form?.success_creating || "System created successfully! Now upload a diagram.",
        status: 'success',
        duration: 3000,
        isClosable: true,
        position: 'top-right',
        variant: 'left-accent'
      });
      
      navigate(`/upload/${id}`);
    } catch (error) {
      toast({
        title: t?.ui?.form?.error_creating_title || "Error",
        description: t.ui.form.error_creating,
        status: 'error',
        duration: 5000,
        isClosable: true,
        position: 'top-right',
        variant: 'left-accent'
      });
    }
  };

  return (
    <Flex align="center" justify="center" height="100vh">
      <Box p={6} borderWidth={1} borderRadius={8} boxShadow="lg" width="400px">
        <Heading mb={4} size="md">{t.ui.form.new_threat_modeling}</Heading>
        {!canWrite && (
          <Alert status="warning" mb={3} borderRadius={6}>
            <AlertIcon />
            {t?.ui?.readonly_warning || "Read-only. You don't have permissions to create information systems."}
          </Alert>
        )}
        <form onSubmit={handleSubmit}>
          <Input
            placeholder={t.ui.form.title_placeholder}
            value={title}
            onChange={e => setTitle(e.target.value)}
            mb={3}
            required
            isDisabled={!canWrite}
          />
          <Textarea
            placeholder={t.ui.form.description_placeholder}
            value={description}
            onChange={e => setDescription(e.target.value)}
            mb={3}
            required
            isDisabled={!canWrite}
          />
          <FormLabel fontSize="sm" mb={1}>{t?.projects?.project || 'Project'}</FormLabel>
          <Box mb={4}>
            <ProjectCombobox
              value={project}
              onChange={setProject}
              isDisabled={!canWrite}
            />
          </Box>
          {canWrite && (
            <Button type="submit" colorScheme="indigo" width="full">{t.ui.form.create_button}</Button>
          )}
        </form>
      </Box>
    </Flex>
  );
};

export default CreateInformationSystem;
