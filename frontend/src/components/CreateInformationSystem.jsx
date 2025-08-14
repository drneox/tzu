import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Flex, Box, Input, Button, Textarea, Heading, useToast } from "@chakra-ui/react";
import { createInformationSystem } from "../services";
import { useLocalization } from '../hooks/useLocalization';

const CreateInformationSystem = () => {
  const { t } = useLocalization();
  const toast = useToast();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [diagram, setDiagram] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Enviar solo los datos, sin imagen
      const data = { title, description };
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
      
      navigate(`/upload/${id}`); // Redirige a la subida de imagen
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
        <form onSubmit={handleSubmit}>
          <Input
            placeholder={t.ui.form.title_placeholder}
            value={title}
            onChange={e => setTitle(e.target.value)}
            mb={3}
            required
          />
          <Textarea
            placeholder={t.ui.form.description_placeholder}
            value={description}
            onChange={e => setDescription(e.target.value)}
            mb={3}
            required
          />
          <Button type="submit" colorScheme="teal" width="full">{t.ui.form.create_button}</Button>
        </form>
      </Box>
    </Flex>
  );
};

export default CreateInformationSystem;
