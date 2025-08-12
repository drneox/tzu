import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Flex, Box, Input, Button, Textarea, Heading } from "@chakra-ui/react";
import { createInformationSystem } from "../services";

const CreateInformationSystem = () => {
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
      navigate(`/upload/${id}`); // Redirige a la subida de imagen
    } catch (error) {
      alert("Error al crear el sistema de información");
    }
  };

  return (
    <Flex align="center" justify="center" height="100vh">
      <Box p={6} borderWidth={1} borderRadius={8} boxShadow="lg" width="400px">
        <Heading mb={4} size="md">Nuevo Threat Modeling</Heading>
        <form onSubmit={handleSubmit}>
          <Input
            placeholder="Título"
            value={title}
            onChange={e => setTitle(e.target.value)}
            mb={3}
            required
          />
          <Textarea
            placeholder="Descripción"
            value={description}
            onChange={e => setDescription(e.target.value)}
            mb={3}
            required
          />
          <Button type="submit" colorScheme="teal" width="full">Crear</Button>
        </form>
      </Box>
    </Flex>
  );
};

export default CreateInformationSystem;
