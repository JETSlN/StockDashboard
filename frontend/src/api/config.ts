/**
 * API Configuration and Base Client
 */

// API base URL - can be configured via environment variables
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// API endpoints
export const API_ENDPOINTS = {
  // Fund endpoints
  FUNDS: '/api/funds',
  FUND_DETAIL: (symbolOrId: string | number) => `/api/funds/${symbolOrId}`,
  FUND_SUMMARY: (symbolOrId: string | number) => `/api/funds/${symbolOrId}/summary`,
  FUND_HOLDINGS: (symbolOrId: string | number) => `/api/funds/${symbolOrId}/holdings`,
  FUND_SECTORS: (symbolOrId: string | number) => `/api/funds/${symbolOrId}/sectors`,
  
  // Price endpoints
  PRICE_HISTORY: (symbolOrId: string | number) => `/api/funds/${symbolOrId}/prices`,
  LATEST_PRICE: (symbolOrId: string | number) => `/api/funds/${symbolOrId}/prices/latest`,
  PRICE_SUMMARY: (symbolOrId: string | number) => `/api/funds/${symbolOrId}/prices/summary`,
} as const;

// HTTP client configuration
export const DEFAULT_HEADERS = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
} as const;

// Custom error class for API errors
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public response?: Response
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// Base API client function
export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config: RequestInit = {
    headers: {
      ...DEFAULT_HEADERS,
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          errorMessage = errorData.detail;
        }
      } catch {
        // If we can't parse the error response, use the default message
      }
      
      throw new APIError(errorMessage, response.status, response);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    
    // Handle network errors, etc.
    throw new APIError(
      error instanceof Error ? error.message : 'Unknown error occurred',
      0
    );
  }
}

// Helper function to build query string
export function buildQueryString(params: Record<string, any>): string {
  const searchParams = new URLSearchParams();
  
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      searchParams.append(key, String(value));
    }
  });
  
  const queryString = searchParams.toString();
  return queryString ? `?${queryString}` : '';
}
