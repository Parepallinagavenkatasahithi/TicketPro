const API_BASE_URL = '/api/v1';

export class APIError extends Error {
  status: number;
  code: string;

  constructor(message: string, status: number, code: string = 'ERROR') {
    super(message);
    this.status = status;
    this.code = code;
  }
}

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem('ticketpro_token');

  const headers: Record<string, string> = {
    'Accept': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  if (token && !headers['Authorization']) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    localStorage.removeItem('ticketpro_token');
    localStorage.removeItem('ticketpro_user');
    if (!window.location.pathname.includes('/login')) {
      window.location.href = '/login';
    }
  }

  if (!response.ok) {
    let errorMessage = 'An unexpected error occurred';
    let errorCode = 'SERVER_ERROR';
    try {
      const errorJson = await response.json();
      if (errorJson.error) {
        errorMessage = errorJson.error.message || errorMessage;
        errorCode = errorJson.error.code || errorCode;
      } else if (errorJson.detail) {
        errorMessage = typeof errorJson.detail === 'string' ? errorJson.detail : JSON.stringify(errorJson.detail);
      }
    } catch (e) {
      errorMessage = response.statusText;
    }
    throw new APIError(errorMessage, response.status, errorCode);
  }

  if (response.status === 204) {
    return {} as T;
  }

  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('text/csv')) {
    const text = await response.text();
    return text as unknown as T;
  }

  return response.json();
}

// API Helper Client Methods
export const api = {
  // Tickets
  getTickets: (params?: Record<string, string>) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    return apiFetch<any[]>(`/tickets${query}`);
  },
  getTicket: (id: number) => apiFetch<any>(`/tickets/${id}`),
  createTicket: (data: any) => apiFetch<any>('/tickets', { method: 'POST', body: JSON.stringify(data) }),
  updateTicketStatus: (id: number, status: string) => apiFetch<any>(`/tickets/${id}/status`, { method: 'PATCH', body: JSON.stringify({ status }) }),
  assignTicket: (id: number, assigned_agent_id: number) => apiFetch<any>(`/tickets/${id}/assign`, { method: 'POST', body: JSON.stringify({ assigned_agent_id }) }),
  addComment: (id: number, content: string, is_internal_note: boolean = false) => apiFetch<any>(`/tickets/${id}/comments`, { method: 'POST', body: JSON.stringify({ content, is_internal_note }) }),

  // Assets
  getAssets: () => apiFetch<any[]>('/assets'),
  createAsset: (data: any) => apiFetch<any>('/assets', { method: 'POST', body: JSON.stringify(data) }),

  // Change Requests
  getChangeRequests: () => apiFetch<any[]>('/change-requests'),
  createChangeRequest: (data: any) => apiFetch<any>('/change-requests', { method: 'POST', body: JSON.stringify(data) }),

  // Problems
  getProblems: () => apiFetch<any[]>('/problems'),
  createProblem: (data: any) => apiFetch<any>('/problems', { method: 'POST', body: JSON.stringify(data) }),

  // Surveys
  getSurveys: () => apiFetch<any[]>('/surveys'),
  submitSurvey: (data: any) => apiFetch<any>('/surveys', { method: 'POST', body: JSON.stringify(data) }),

  // Time Tracking
  getTimeEntries: (ticketId: number) => apiFetch<any[]>(`/time-tracking/tickets/${ticketId}`),
  logTime: (data: any) => apiFetch<any>('/time-tracking', { method: 'POST', body: JSON.stringify(data) }),

  // Vendors & Licenses
  getVendors: () => apiFetch<any[]>('/vendors'),
  createVendor: (data: any) => apiFetch<any>('/vendors', { method: 'POST', body: JSON.stringify(data) }),
  getSoftwareLicenses: () => apiFetch<any[]>('/vendors/licenses'),
  createSoftwareLicense: (data: any) => apiFetch<any>('/vendors/licenses', { method: 'POST', body: JSON.stringify(data) }),

  // Contracts
  getContracts: () => apiFetch<any[]>('/contracts'),
  createContract: (data: any) => apiFetch<any>('/contracts', { method: 'POST', body: JSON.stringify(data) }),

  // On-Call
  getOnCallRotations: () => apiFetch<any[]>('/on-call'),
  createOnCallRotation: (data: any) => apiFetch<any>('/on-call', { method: 'POST', body: JSON.stringify(data) }),
  createOnCallShift: (data: any) => apiFetch<any>('/on-call/shifts', { method: 'POST', body: JSON.stringify(data) }),

  // Service Catalog
  getServiceCatalogCategories: () => apiFetch<any[]>('/service-catalog/categories'),
  getServiceCatalogItems: () => apiFetch<any[]>('/service-catalog/items'),

  // Custom Fields & Templates
  getCustomFields: (entity: string = 'TICKET') => apiFetch<any[]>(`/custom-fields?target_entity=${entity}`),
  getEmailTemplates: () => apiFetch<any[]>('/email-templates'),

  // Dashboard & Analytics
  getDashboardMetrics: () => apiFetch<any>('/analytics/dashboard'),
  getTicketTrends: (days: number = 30) => apiFetch<any[]>(`/analytics/trends?days=${days}`),
  getPriorityDistribution: () => apiFetch<any[]>('/analytics/priority-distribution')
};

