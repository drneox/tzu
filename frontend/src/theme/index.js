import { extendTheme } from '@chakra-ui/react';
import { palette, colors } from './colors';

/**
 * Tema personalizado de Chakra UI para TZU standalone.
 * Extiende la paleta default añadiendo 'indigo', 'slate' y 'teal' como escalas nombradas,
 * y configura componentes base para un look limpio y minimalista.
 */
const theme = extendTheme({
  colors: {
    teal: palette.teal,
    indigo: palette.indigo,
    slate: palette.slate,
  },

  fonts: {
    heading: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    body: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
  },

  styles: {
    global: {
      body: {
        bg: 'slate.50',
        color: 'slate.800',
      },
    },
  },

  components: {
    Button: {
      defaultProps: {
        colorScheme: 'indigo',
      },
      variants: {
        solid: {
          bg: 'indigo.500',
          color: 'white',
          _hover: {
            bg: 'indigo.600',
            _disabled: {
              bg: 'indigo.500',
            },
          },
        },
        ghost: {
          color: 'slate.700',
          _hover: {
            bg: 'slate.100',
          },
        },
      },
    },

    Heading: {
      baseStyle: {
        color: 'slate.800',
        letterSpacing: '-0.025em',
      },
    },

    Card: {
      baseStyle: {
        container: {
          bg: 'white',
          borderColor: 'slate.200',
        },
      },
    },

    Input: {
      defaultProps: {
        focusBorderColor: 'indigo.500',
      },
      variants: {
        outline: {
          field: {
            bg: 'slate.50',
            borderColor: 'slate.200',
            _hover: {
              borderColor: 'slate.300',
            },
            _focus: {
              borderColor: 'indigo.500',
              boxShadow: `0 0 0 1px ${colors.primary.default}`,
            },
          },
        },
      },
    },

    Badge: {
      baseStyle: {
        borderRadius: 'full',
        px: 2,
        py: 0.5,
      },
    },
  },
});

export default theme;
