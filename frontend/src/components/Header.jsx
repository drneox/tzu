import React from "react";
import { Heading, Flex, Divider } from "@chakra-ui/react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <Flex
      as="nav"
      align="center"
      wrap="wrap"
      padding="0.5rem"
      bg="#00243c"
      color="#ffa833"
    >
      <Flex direction="column" align="left" width="100%">
        <Heading as="h1" size="xl" display="flex" flexDirection="row" textAlign="center" alignItems="center" >
          <div>
            <img className="header_image" src="/tzu.png" alt="logo" width="100vh" />
          </div>
          <div> <h1>Threat Zero Utility</h1></div>
        </Heading>
        <Flex 
          width="200px"
          justifyContent="space-between"
          mt={4}
        >
          <Link to="/create" style={{ textDecoration: 'none', color: '#ffa833' }}>
            <h3>Nuevo Analisis</h3>
          </Link>
          <Link to="/" style={{ textDecoration: 'none', color: '#ffa833' }}>
            <h3>Archivo</h3>
          </Link>
        </Flex>
      </Flex>
    </Flex>
  );
};

export default Header;