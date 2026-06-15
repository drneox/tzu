/**
 * TZU Standalone — Design tokens de color (única fuente de verdad)
 * Paleta: clara y minimalista (SaaS clean)
 *
 * Regla: ningún componente debe usar hex codes hardcodeados. Usar siempre
 * los tokens exportados aquí o los valores registrados en theme/index.js
 * (indigo.xxx, slate.xxx, etc.) vía Chakra UI.
 */

export const palette = {
  // Teal disponible como escala adicional
  teal: {
    50: '#f0fdfa',
    100: '#ccfbf1',
    200: '#99f6e4',
    300: '#5eead4',
    400: '#2dd4bf',
    500: '#14b8a6',
    600: '#0d9488',
    700: '#0f766e',
    800: '#115e59',
    900: '#134e4a',
  },

  brand: '#3f2ed2',

  // Índigo disponible como acento secundario si se necesita
  indigo: {
    50: '#eef2ff',
    100: '#e0e7ff',
    200: '#c7d2fe',
    300: '#a5b4fc',
    400: '#818cf8',
    500: '#6366f1',
    600: '#4f46e5',
    700: '#3f2ed2',
    800: '#3730a3',
    900: '#312e81',
  },

  // Neutros: slate en lugar de gray puro
  slate: {
    50: '#f8fafc',
    100: '#f1f5f9',
    200: '#e2e8f0',
    300: '#cbd5e1',
    400: '#94a3b8',
    500: '#64748b',
    600: '#475569',
    700: '#334155',
    800: '#1e293b',
    900: '#0f172a',
  },

  // Riesgo: tonos limpios y accesibles
  risk: {
    critical: '#e11d48', // rose.600
    high: '#f97316',     // orange.500
    medium: '#eab308',   // yellow.500
    low: '#10b981',      // emerald.500
    unknown: '#64748b',  // slate.500
  },

  // Semánticos auxiliares
  success: '#10b981',
  warning: '#f59e0b',
  error: '#e11d48',
  info: '#3b82f6',

  // Varios
  white: '#ffffff',
  black: '#000000',
  transparent: 'transparent',
};

// Tokens de alto nivel. Preferir usar estos en lugar de palette directamente.
export const colors = {
  transparent: palette.transparent,
  brand: palette.brand,
  background: palette.slate[50],
  surface: palette.white,
  border: palette.slate[200],
  borderSubtle: palette.slate[100],
  borderStrong: palette.slate[300],

  risk: palette.risk,

  text: {
    primary: palette.slate[800],
    secondary: palette.slate[600],
    muted: palette.slate[400],
    onPrimary: palette.white,
    dark: '#333333',
    medium: '#666666',
    light: '#999999',
  },

  primary: {
    default: palette.indigo[600],
    hover: palette.indigo[700],
    light: palette.indigo[50],
    subtle: palette.indigo[100],
  },

  header: {
    bg: palette.white,
    text: palette.slate[800],
    accent: palette.indigo[600],
    border: palette.slate[200],
  },

  footer: {
    bg: palette.white,
    text: palette.slate[500],
    border: palette.slate[200],
  },

  login: {
    bg: palette.slate[50],
    cardBg: palette.white,
    title: palette.slate[800],
    subtitle: palette.slate[500],
    inputBorder: palette.slate[200],
    inputBg: palette.slate[50],
  },

  nav: {
    inactiveText: palette.slate[500],
    activeText: palette.indigo[700],
    activeBg: palette.indigo[100],
    hoverBg: palette.slate[100],
    hoverText: palette.slate[700],
  },

  chart: {
    asvs: palette.indigo[500],
    masvs: '#8b5cf6', // violet.500
    iso27001: palette.success,
    nist: palette.warning,
    sbs: '#06b6d4', // cyan.500
  },

  chartLight: {
    asvs: palette.indigo[100],
    masvs: '#ede9fe', // violet.100
    iso27001: '#d1fae5', // emerald.100
    nist: '#fef3c7', // amber.100
    sbs: '#cffafe', // cyan.100
  },

  controlTag: {
    tagBg: palette.indigo[600],
    tagText: palette.white,
    inputBorder: '#cccccc',
    inputBorderFilled: palette.indigo[600],
    panelBg: palette.slate[50],
    panelBorder: palette.slate[200],
  },

  riskDisplay: {
    bg: palette.slate[50],
  },

  owasp: {
    threatAgent: {
      bg: 'blue.100',
      border: '#4299e1',
      text: 'blue.800',
      lightBg: 'blue.50',
    },
    vulnerability: {
      bg: 'orange.100',
      border: '#ed8936',
      text: 'orange.800',
      lightBg: 'orange.50',
    },
    technicalImpact: {
      bg: 'red.100',
      border: '#e53e3e',
      text: 'red.800',
      lightBg: 'red.50',
    },
    businessImpact: {
      bg: 'purple.100',
      border: '#805ad5',
      text: 'purple.800',
      lightBg: 'purple.50',
    },
  },

  table: {
    headerBg: palette.slate[50],
    headerText: palette.slate[700],
    border: palette.slate[200],
    cellText: palette.slate[600],
  },
};

export default colors;
