import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Flex, Box, Input, Button, Heading } from "@chakra-ui/react";
import { uploadDiagram } from "../services";

const UploadDiagram = () => {
  const { id } = useParams();
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    try {
      await uploadDiagram(id, file);
      navigate("/");
    } catch (error) {
      alert("Error al subir la imagen");
    }
  };

  return (
    <Flex align="center" justify="center" height="100vh">
      <Box p={6} borderWidth={1} borderRadius={8} boxShadow="lg" width="400px">
        <Heading mb={4} size="md">Subir Diagrama</Heading>
        <form onSubmit={handleSubmit} encType="multipart/form-data">
          <Input
            type="file"
            accept="image/*"
            mb={3}
            onChange={e => setFile(e.target.files[0])}
            required
          />
          <Button type="submit" colorScheme="teal" width="full">Subir</Button>
        </form>
      </Box>
    </Flex>
  );
};

export default UploadDiagram;
