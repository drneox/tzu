import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {getInformationSystems} from "../services";
import { Flex, TableContainer, Table, Tr,Td, Thead, Th, Tbody } from "@chakra-ui/react";
const Index = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [serviceData, setServiceData] = useState([]);
  useEffect(() =>{
    getInformationSystems().then((res) => {
        setServiceData(res.data)
        setIsLoading(false);
    }
    
);


  },[])
  if (isLoading){
    return (
        <div className="App">
          <h1>Cargando...</h1>
        </div>
      );
    } else {
      return (
        <Flex
          as="nav"
          align="center"
          wrap="wrap"
          padding="0.5rem"
          justify="center"
          style={{ marginBottom: "160px" }}
        >
          <TableContainer>
            <Table border="2px solid gray" borderCollapse="collapse" variant='striped' colorScheme='gray' overflowX='auto' whiteSpace='normal' width='600px'>
              <Thead>
                <Tr bg="gray.300" color="white" p="4">
                  <Th p="1" shadow="md">Título</Th>
                  <Th p="1" shadow="md" maxWidth='100px'>Descripción</Th>
                  <Th p="1" shadow="md" maxWidth='100px'>Fecha</Th>
                </Tr>
              </Thead>
              <Tbody>
                {serviceData.map(data => {
                  const dateTime = new Date(data.datetime).toLocaleString();
                  return (
                    <Tr key={data.id}>
                      <Td><Link to={`analysis/${data.id}`}>{String(data.title)}</Link></Td>
                      <Td>{data.description}</Td>
                      <Td>{dateTime}</Td>
                    </Tr>
                  );
                })}
              </Tbody>
            </Table>
          </TableContainer>
        </Flex>
      );
    }
}
export default Index;