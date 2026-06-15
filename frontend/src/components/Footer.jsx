import React from "react";
import { Flex, Text, Link } from "@chakra-ui/react";
import { colors } from '../theme/colors';

const version = process.env.REACT_APP_VERSION || '';

const year = new Date().getFullYear();

const Footer = () => {
  return (
    <Flex
      as="footer"
      bg={colors.footer.bg}
      color={colors.footer.text}
      justify="center"
      align="center"
      position="fixed"
      bottom="0"
      width="100%"
      h="36px"
      borderTop={`1px solid ${colors.footer.border}`}
      fontSize="sm"
    >
      <Text opacity={0.8}>
        © {year} TZU Security v{version} —{" "}
        <Link href="https://tzusecurity.com" isExternal color="indigo.600" _hover={{ color: 'indigo.700' }}>
          tzusecurity.com
        </Link>
      </Text>
    </Flex>
  );
};

export default Footer;
