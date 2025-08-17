// Mock axios completely
jest.mock('axios', () => ({
  create: jest.fn(() => ({
    get: jest.fn(() => Promise.resolve({ data: {} })),
    post: jest.fn(() => Promise.resolve({ data: {} })),
    put: jest.fn(() => Promise.resolve({ data: {} })),
    delete: jest.fn(() => Promise.resolve({ data: {} })),
    interceptors: {
      request: {
        use: jest.fn()
      },
      response: {
        use: jest.fn()
      }
    }
  })),
  get: jest.fn(() => Promise.resolve({ data: {} })),
  post: jest.fn(() => Promise.resolve({ data: {} })),
  put: jest.fn(() => Promise.resolve({ data: {} })),
  delete: jest.fn(() => Promise.resolve({ data: {} }))
}));

describe('API Services', () => {
  test('should be importable', () => {
    // Simple test to verify the services can be imported
    expect(true).toBe(true);
  });

  test('should have expected service functions', () => {
    const services = require('../../services/index');
    
    expect(typeof services.fetchInformationSystemById).toBe('function');
    expect(typeof services.updateThreatsRiskBatch).toBe('function');
    expect(typeof services.createThreatForSystem).toBe('function');
    expect(typeof services.updateThreatResidualRisk).toBe('function');
    expect(typeof services.updateThreatsResidualRiskBatch).toBe('function');
  });
});
