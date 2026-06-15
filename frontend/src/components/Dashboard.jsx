/**
 * Security Dashboard Component
 * Archivo: Dashboard.jsx
 *
 * Secciones:
 * - KPI Cards          (T008 / US1 / FR-002)
 * - Risk PieChart      (T009 / US1 / FR-003)
 * - Project Filter     (T010 / US1 / FR-005)
 * - Empty State        (T011 / US1 / FR-007)
 * - Loading Skeletons  (T012 / US1 / FR-008) — todas las secciones
 * - Top-5 Systems      (T013-T014 / US2 / FR-004)
 * - Trends Placeholder (T015 / US3 / FR-009)
 * - Standards Chart    (T016-T017 / US4 / FR-006)
 * - Error States       (T018 / FR-008)
 */

import React, { useState, useEffect, useCallback } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Button,
  Flex,
  Grid,
  GridItem,
  Heading,
  Select,
  Skeleton,
  Stat,
  StatLabel,
  StatNumber,
  Table,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
  Alert,
  AlertIcon,
  AlertTitle,
  Badge,
} from '@chakra-ui/react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from 'recharts';

import { getDashboardStats } from '../services/apiClient';
import { getProjects } from '../services/projectService';
import { useLocalization } from '../hooks/useLocalization';
import { colors } from '../theme/colors';
import { getRiskLevelColor } from '../utils/riskCalculations';

// ── Colour palette ────────────────────────────────────────────────────────────
const RISK_COLORS = {
  CRITICAL: getRiskLevelColor('CRITICAL'),
  HIGH: getRiskLevelColor('HIGH'),
  MEDIUM: getRiskLevelColor('MEDIUM'),
  LOW: getRiskLevelColor('LOW'),
  UNKNOWN: getRiskLevelColor('UNKNOWN'),
};

const STANDARD_COLORS = {
  ASVS:     colors.chart.asvs,
  MASVS:    colors.chart.masvs,
  ISO27001: colors.chart.iso27001,
  NIST:     colors.chart.nist,
  SBS:      colors.chart.sbs,
};

const STANDARD_COLORS_LIGHT = {
  ASVS:     colors.chartLight.asvs,
  MASVS:    colors.chartLight.masvs,
  ISO27001: colors.chartLight.iso27001,
  NIST:     colors.chartLight.nist,
  SBS:      colors.chartLight.sbs,
};

// ── Helper: small KPI card ────────────────────────────────────────────────────
const KpiCard = ({ label, value, color }) => (
  <Box p={4} borderWidth="1px" borderRadius="lg" bg="white" boxShadow="sm" minW="0">
    <Stat>
      <StatLabel fontSize="xs" color="gray.500" isTruncated>
        {label}
      </StatLabel>
      <StatNumber fontSize="xl" color={color || 'inherit'}>
        {value ?? '—'}
      </StatNumber>
    </Stat>
  </Box>
);

// ── Section error helper ──────────────────────────────────────────────────────
const SectionError = ({ message, onRetry }) => (
  <Alert status="error" borderRadius="md">
    <AlertIcon />
    <Box flex="1">
      <AlertTitle fontSize="sm">{message}</AlertTitle>
    </Box>
    {onRetry && (
      <Button onClick={onRetry} size="xs" ml={2} flexShrink={0}>
        Retry
      </Button>
    )}
  </Alert>
);

// ── Main component ────────────────────────────────────────────────────────────
const Dashboard = () => {
  const { t } = useLocalization();
  const tb = t?.dashboard;

  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [projects, setProjects] = useState([]);
  const [projectsLoading, setProjectsLoading] = useState(true);
  const [selectedProject, setSelectedProject] = useState('');

  // ── Fetch dashboard stats ────────────────────────────────────────────────
  const fetchStats = useCallback(async (projectId) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getDashboardStats(projectId || null);
      setStats(data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, []);

  // ── On mount: load projects + initial stats ──────────────────────────────
  useEffect(() => {
    const loadProjects = async () => {
      try {
        const res = await getProjects(0, 100);
        setProjects(res.data || []);
      } catch (_) {
        // projects fail silently — filter section just won't show options
      } finally {
        setProjectsLoading(false);
      }
    };
    loadProjects();
    fetchStats(null);
  }, [fetchStats]);

  const handleProjectChange = (e) => {
    const pid = e.target.value;
    setSelectedProject(pid);
    fetchStats(pid || null);
  };

  // ── Derived state ────────────────────────────────────────────────────────
  const isEmpty = !loading && !error && stats && stats.total_systems === 0;

  const pieData = stats
    ? Object.entries(stats.threats_by_level)
        .map(([name, value]) => ({ name, value }))
        .filter((d) => d.value > 0)
    : [];

  const barData = stats
    ? Object.entries(stats.standards_coverage).map(([name, coverage]) => ({
        name,
        coverage,
        remediation: stats.standards_remediation?.[name] ?? 0,
      }))
    : [];

  const allZeroCoverage = barData.length > 0 && barData.every((d) => d.coverage === 0);

  // ── Render ───────────────────────────────────────────────────────────────
  return (
    <Box p={6} maxW="1280px" mx="auto">
      {/* ── Header + Project Filter (T010) ─────────────────────────────── */}
      <Flex justify="space-between" align="center" mb={6} wrap="wrap" gap={3}>
        <Heading size="lg">{tb?.title || 'Security Dashboard'}</Heading>
        <Select
          placeholder={tb?.filter_all || 'All projects'}
          value={selectedProject}
          onChange={handleProjectChange}
          maxW="280px"
          size="sm"
          isDisabled={projectsLoading}
        >
          {projects.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </Select>
      </Flex>

      {/* ── Empty State (T011) ─────────────────────────────────────────── */}
      {isEmpty && (
        <Box textAlign="center" py={20} px={4}>
          <Heading size="md" mb={3}>
            {tb?.empty_title || 'No systems registered yet'}
          </Heading>
          <Text color="gray.500" mb={5}>
            {tb?.empty_body || 'Start by creating your first information system.'}
          </Text>
          <Button as={RouterLink} to="/create" colorScheme="indigo" size="md">
            {tb?.empty_cta || 'Create Information System'}
          </Button>
        </Box>
      )}

      {/* ── Main Grid — shown when not empty and no global error ───────── */}
      {!isEmpty && (
        <Grid templateColumns={{ base: '1fr', lg: 'repeat(2, 1fr)' }} gap={6}>
          {/* KPI Cards (T008) */}
          <GridItem colSpan={{ base: 1, lg: 2 }}>
            <Heading size="sm" mb={3}>
              {tb?.kpis?.title || 'Security Overview'}
            </Heading>
            {error ? (
              <SectionError
                message={tb?.error_body || 'Could not load dashboard statistics.'}
                onRetry={() => fetchStats(selectedProject || null)}
              />
            ) : (
              <Skeleton isLoaded={!loading} borderRadius="md">
                <Grid
                  templateColumns="repeat(auto-fill, minmax(150px, 1fr))"
                  gap={4}
                >
                  <KpiCard
                    label={tb?.kpis?.total_systems || 'Systems'}
                    value={stats?.total_systems}
                  />
                  <KpiCard
                    label={tb?.kpis?.total_threats || 'Threats'}
                    value={stats?.total_threats}
                  />
                  <KpiCard
                    label={tb?.kpis?.critical || 'Critical'}
                    value={stats?.threats_by_level?.CRITICAL}
                    color="red.500"
                  />
                  <KpiCard
                    label={tb?.kpis?.high || 'High'}
                    value={stats?.threats_by_level?.HIGH}
                    color="orange.400"
                  />
                  <KpiCard
                    label={tb?.kpis?.remediation_rate || 'Remediation Rate'}
                    value={stats ? `${stats.remediation_rate}%` : '—'}
                    color="green.500"
                  />
                </Grid>
              </Skeleton>
            )}
          </GridItem>

          {/* Risk Distribution PieChart (T009) */}
          <GridItem>
            <Heading size="sm" mb={3}>
              {tb?.risk_chart?.title || 'Risk Distribution'}
            </Heading>
            {error ? (
              <SectionError
                message={tb?.error_body || 'Could not load risk distribution.'}
                onRetry={() => fetchStats(selectedProject || null)}
              />
            ) : (
              <Skeleton isLoaded={!loading} borderRadius="md" minH="280px">
                <Box h="280px">
                  {pieData.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={pieData}
                          cx="50%"
                          cy="50%"
                          outerRadius={100}
                          dataKey="value"
                          label={({ name, percent }) =>
                            `${name} ${(percent * 100).toFixed(0)}%`
                          }
                        >
                          {pieData.map((entry) => (
                            <Cell
                              key={entry.name}
                              fill={RISK_COLORS[entry.name] || colors.risk.unknown}
                            />
                          ))}
                        </Pie>
                        <Tooltip formatter={(val, name) => [val, name]} />
                      </PieChart>
                    </ResponsiveContainer>
                  ) : (
                    <Flex h="100%" align="center" justify="center">
                      <Text color="gray.400">
                        {tb?.risk_chart?.no_data || 'No threat data available'}
                      </Text>
                    </Flex>
                  )}
                </Box>
              </Skeleton>
            )}
          </GridItem>

          {/* Top-5 Projects / Top-5 Systems Table (T013 / T014) */}
          <GridItem>
            <Heading size="sm" mb={3}>
              {selectedProject
                ? (tb?.top_systems?.title || 'Evaluations with most Threats (Top 5)')
                : (tb?.top_projects?.title || 'Projects with most Threats (Top 5)')}
            </Heading>
            {error ? (
              <SectionError
                message={tb?.error_body || 'Could not load data.'}
                onRetry={() => fetchStats(selectedProject || null)}
              />
            ) : (
              <Skeleton isLoaded={!loading} borderRadius="md" minH="280px">
                {/* ── When project selected: top evaluations ── */}
                {selectedProject && (
                  stats?.top_systems?.length > 0 ? (
                    <Table size="sm" variant="simple">
                      <Thead>
                        <Tr>
                          <Th>{tb?.top_systems?.system_col || 'Evaluation'}</Th>
                          <Th isNumeric color="red.500">
                            {tb?.top_systems?.critical_col || 'CRIT'}
                          </Th>
                          <Th isNumeric color="orange.400">
                            {tb?.top_systems?.high_col || 'HIGH'}
                          </Th>
                          <Th isNumeric>{tb?.top_systems?.total_col || 'Total'}</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        {stats.top_systems.map((sys) => {
                          const hasRisk = sys.critical_count > 0 || sys.high_count > 0;
                          return (
                            <Tr key={sys.id}>
                              <Td>
                                <RouterLink
                                  to={`/analysis/${sys.id}`}
                                  style={{ color: colors.primary.default, textDecoration: 'underline' }}
                                >
                                  {sys.title}
                                </RouterLink>
                              </Td>
                              <Td isNumeric>
                                {hasRisk ? (
                                  <Badge colorScheme={sys.critical_count > 0 ? 'red' : 'gray'}>
                                    {sys.critical_count}
                                  </Badge>
                                ) : (
                                  <Text fontSize="xs" color="gray.400">—</Text>
                                )}
                              </Td>
                              <Td isNumeric>
                                {hasRisk ? (
                                  <Badge colorScheme={sys.high_count > 0 ? 'orange' : 'gray'}>
                                    {sys.high_count}
                                  </Badge>
                                ) : (
                                  <Text fontSize="xs" color="gray.400">—</Text>
                                )}
                              </Td>
                              <Td isNumeric>{sys.total_threats}</Td>
                            </Tr>
                          );
                        })}
                      </Tbody>
                    </Table>
                  ) : (
                    <Flex minH="280px" align="center" justify="center">
                      <Text color="gray.400">
                        {tb?.top_systems?.no_data || 'No exposed evaluations'}
                      </Text>
                    </Flex>
                  )
                )}

                {/* ── When no project selected: top projects ── */}
                {!selectedProject && (
                  stats?.top_projects?.length > 0 ? (
                    <Table size="sm" variant="simple">
                      <Thead>
                        <Tr>
                          <Th>{tb?.top_projects?.project_col || 'Project'}</Th>
                          <Th isNumeric color="red.500">
                            {tb?.top_projects?.critical_col || 'CRIT'}
                          </Th>
                          <Th isNumeric color="orange.400">
                            {tb?.top_projects?.high_col || 'HIGH'}
                          </Th>
                          <Th isNumeric>{tb?.top_projects?.total_col || 'Total'}</Th>
                          <Th isNumeric>{tb?.top_projects?.systems_col || 'Evaluations'}</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        {stats.top_projects.map((proj, idx) => {
                          const hasRisk = proj.critical_count > 0 || proj.high_count > 0;
                          return (
                            <Tr key={proj.id || `__none_${idx}`}>
                              <Td fontWeight="medium">{proj.name}</Td>
                              <Td isNumeric>
                                {hasRisk ? (
                                  <Badge colorScheme={proj.critical_count > 0 ? 'red' : 'gray'}>
                                    {proj.critical_count}
                                  </Badge>
                                ) : (
                                  <Text fontSize="xs" color="gray.400">—</Text>
                                )}
                              </Td>
                              <Td isNumeric>
                                {hasRisk ? (
                                  <Badge colorScheme={proj.high_count > 0 ? 'orange' : 'gray'}>
                                    {proj.high_count}
                                  </Badge>
                                ) : (
                                  <Text fontSize="xs" color="gray.400">—</Text>
                                )}
                              </Td>
                              <Td isNumeric>{proj.total_threats}</Td>
                              <Td isNumeric>{proj.system_count}</Td>
                            </Tr>
                          );
                        })}
                      </Tbody>
                    </Table>
                  ) : (
                    <Flex minH="280px" align="center" justify="center">
                      <Text color="gray.400">
                        {tb?.top_projects?.no_data || 'No projects with threats'}
                      </Text>
                    </Flex>
                  )
                )}
              </Skeleton>
            )}
          </GridItem>

          {/* Standards Coverage BarChart (T016 / T017) */}
          <GridItem colSpan={{ base: 1, lg: 2 }}>
            <Heading size="sm" mb={3}>
              {tb?.standards?.title || 'Standards Coverage'}
            </Heading>
            {error ? (
              <SectionError
                message={tb?.error_body || 'Could not load standards coverage.'}
                onRetry={() => fetchStats(selectedProject || null)}
              />
            ) : (
              <Skeleton isLoaded={!loading} borderRadius="md" minH="220px">
                <Box>
                  <Box h="220px">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={barData}
                        margin={{ top: 5, right: 20, left: 0, bottom: 5 }}
                        barCategoryGap="20%"
                        barGap={2}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                        <YAxis
                          domain={[0, 100]}
                          tickFormatter={(v) => `${v}%`}
                          tick={{ fontSize: 12 }}
                        />
                        <Tooltip
                          formatter={(v, name) => [
                            `${v.toFixed(1)}%`,
                            name === 'coverage'
                              ? (tb?.standards?.legend_coverage || 'Cobertura')
                              : (tb?.standards?.legend_remediation || 'Remediadas'),
                          ]}
                        />
                        <Legend
                          formatter={(value) =>
                            value === 'coverage'
                              ? (tb?.standards?.legend_coverage || 'Cobertura')
                              : (tb?.standards?.legend_remediation || 'Remediadas')
                          }
                        />
                        <Bar dataKey="coverage" radius={[4, 4, 0, 0]}>
                          {barData.map((entry) => (
                            <Cell
                              key={`cov-${entry.name}`}
                              fill={STANDARD_COLORS[entry.name] || colors.risk.unknown}
                            />
                          ))}
                        </Bar>
                        <Bar dataKey="remediation" radius={[4, 4, 0, 0]}>
                          {barData.map((entry) => (
                            <Cell
                              key={`rem-${entry.name}`}
                              fill={STANDARD_COLORS_LIGHT[entry.name] || colors.borderStrong}
                            />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                  {allZeroCoverage && (
                    <Text
                      textAlign="center"
                      color="gray.400"
                      fontSize="sm"
                      mt={2}
                    >
                      {tb?.standards?.no_tags ||
                        'No hay controles asignados aún'}
                    </Text>
                  )}
                </Box>
              </Skeleton>
            )}
          </GridItem>

          {/* Historical Trends Placeholder (T015) */}
          <GridItem colSpan={{ base: 1, lg: 2 }}>
            <Heading size="sm" mb={3}>
              {tb?.trends?.title || 'Historical Trends'}
            </Heading>
            <Box
              p={6}
              borderWidth="1px"
              borderRadius="md"
              borderStyle="dashed"
              borderColor="gray.300"
              textAlign="center"
              bg="gray.50"
            >
              <Text color="gray.400" fontSize="sm">
                {tb?.trends?.placeholder ||
                  'El historial de tendencias estará disponible en una versión futura'}
              </Text>
            </Box>
          </GridItem>
        </Grid>
      )}
    </Box>
  );
};

export default Dashboard;
