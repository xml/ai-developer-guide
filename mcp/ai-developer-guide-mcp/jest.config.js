export default {
  preset: 'ts-jest/presets/default-esm',
  extensionsToTreatAsEsm: ['.ts'],
  testEnvironment: 'node',
  moduleNameMapper: {
    '^(\\.{1,2}/.*)\\.js$': '$1',
  },
  transform: {
    '^.+\\.ts$': ['ts-jest', {
      useESM: true,
    }],
  },
  setupFilesAfterEnv: ['<rootDir>/src/test-setup.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.spec.ts',
    '!src/**/*.test.ts',
    '!src/test-setup.ts',
    '!src/cli.ts',
  ],
  coverageDirectory: 'artifacts/coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  testMatch: ['**/*.spec.ts', '**/*.test.ts'],
  clearMocks: true,
  resetMocks: true,
  restoreMocks: true,
}; 