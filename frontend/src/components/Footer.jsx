import React from "react";
import { Heading, Flex } from "@chakra-ui/react";


const Footer = () => {
  return (
    <Flex
      bg="#00243c"
      color="#ffa833"
      justify="center"
      position="fixed"
      bottom="0"
      width="100%"
    >
      <Flex align="center">
        <div as="h1" size="xl" flex-direction="row" text-align="center" >
          <div> <h1>Coded by Carlos Ganoza</h1></div>
        </div>
      </Flex>
    </Flex>
  );
};

export default Footer;