// Jest test setup file
import { jest, beforeEach } from '@jest/globals';

// Mock fetch globally
global.fetch = jest.fn() as jest.MockedFunction<typeof fetch>;

// Reset mocks before each test
beforeEach(() => {
  jest.clearAllMocks();
}); 