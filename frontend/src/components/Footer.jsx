import React from "react";
import { Flex, Text, Link } from "@chakra-ui/react";

const version = process.env.REACT_APP_VERSION || '';

const year = new Date().getFullYear();

const Footer = () => {
  return (
    <Flex
      as="footer"
      bg="#00243c"
      color="#ffa833"
      justify="center"
      align="center"
      position="fixed"
      bottom="0"
      width="100%"
      h="36px"
      borderTop="1px solid rgba(255,168,51,0.15)"
    >
      <Text fontSize="sm" opacity={0.8}>
        © {year} TZU Security v{version} —{" "}
        <Link href="https://tzusecurity.com" isExternal color="#ffa833" _hover={{ opacity: 1 }}>
          tzusecurity.com
        </Link>
      </Text>
    </Flex>
  );
};

export default Footer;