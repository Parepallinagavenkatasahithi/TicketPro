export type RoleName = 'ADMIN' | 'MANAGER' | 'AGENT' | 'EMPLOYEE';

export interface User {
  id: number;
  employee_id: string;
  email: string;
  full_name: string;
  job_title?: string;
  phone?: string;
  avatar_url?: string;
  role_id: number;
  role_name: RoleName;
  department_id?: number;
  department_name?: string;
  is_active: boolean;
  is_verified: boolean;
  last_login_at?: string;
  created_at: string;
}

export type TicketStatusType = 
  | 'NEW'
  | 'OPEN'
  | 'ASSIGNED'
  | 'IN_PROGRESS'
  | 'WAITING_FOR_USER'
  | 'WAITING_FOR_APPROVAL'
  | 'RESOLVED'
  | 'CLOSED'
  | 'REOPENED'
  | 'CANCELLED';

export type TicketPriorityType = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface TicketCategory {
  id: number;
  name: string;
  description?: string;
  default_priority: TicketPriorityType;
  default_department_id?: number;
  icon_name?: string;
  is_active: boolean;
}

export interface Ticket {
  id: number;
  ticket_number: string;
  title: string;
  description: string;
  category_id: number;
  category_name?: string;
  priority: TicketPriorityType;
  status: TicketStatusType;
  requester_id: number;
  requester_name?: string;
  requester_email?: string;
  assigned_agent_id?: number;
  assigned_agent_name?: string;
  department_id: number;
  department_name?: string;
  sla_policy_id?: number;
  first_response_due_at?: string;
  first_responded_at?: string;
  first_response_breached: boolean;
  resolution_due_at?: string;
  resolved_at?: string;
  resolution_breached: boolean;
  closed_at?: string;
  is_overdue: boolean;
  contact_method: string;
  created_at: string;
  updated_at: string;
}

export interface TicketComment {
  id: number;
  ticket_id: number;
  author_id: number;
  author_name: string;
  author_role: RoleName;
  author_avatar?: string;
  content: string;
  is_internal_note: boolean;
  created_at: string;
  updated_at: string;
}

export interface TicketAttachment {
  id: number;
  ticket_id: number;
  comment_id?: number;
  uploader_id: number;
  uploader_name: string;
  file_name: string;
  storage_path: string;
  file_size: number;
  mime_type: string;
  created_at: string;
}

export interface TicketHistory {
  id: number;
  actor_id: number;
  actor_name?: string;
  event_type: string;
  old_value?: string;
  new_value?: string;
  description?: string;
  created_at: string;
}

export interface TicketDetail extends Ticket {
  comments: TicketComment[];
  attachments: TicketAttachment[];
  history: TicketHistory[];
}

export interface Department {
  id: number;
  name: string;
  code: string;
  description?: string;
  manager_id?: number;
  manager_name?: string;
  member_count: number;
  open_ticket_count: number;
  created_at: string;
}

export interface SLAPolicy {
  id: number;
  name: string;
  description?: string;
  priority: TicketPriorityType;
  max_first_response_minutes: number;
  max_resolution_minutes: number;
  warning_threshold_percent: number;
  is_default: boolean;
  is_active: boolean;
  created_at: string;
}

export interface ApprovalStep {
  id: number;
  step_number: number;
  approver_id: number;
  approver_name: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  decision_notes?: string;
  decided_at?: string;
}

export interface ApprovalRequest {
  id: number;
  ticket_id: number;
  ticket_number: string;
  requester_id: number;
  requester_name: string;
  title: string;
  rationale?: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'CANCELLED';
  created_at: string;
  steps: ApprovalStep[];
}

export interface Announcement {
  id: number;
  title: string;
  content: string;
  priority: 'NORMAL' | 'IMPORTANT' | 'URGENT';
  target_audience: string;
  status: 'DRAFT' | 'PUBLISHED' | 'SCHEDULED' | 'ARCHIVED';
  author_id: number;
  author_name: string;
  published_at?: string;
  scheduled_for?: string;
  created_at: string;
}

export interface NotificationItem {
  id: number;
  user_id: number;
  title: string;
  message: string;
  notification_type: string;
  reference_id?: string;
  is_read: boolean;
  read_at?: string;
  created_at: string;
}

export interface KBArticle {
  id: number;
  title: string;
  slug: string;
  category_id?: number;
  category_name?: string;
  content: string;
  author_id: number;
  author_name: string;
  status: string;
  view_count: number;
  helpful_count: number;
  unhelpful_count: number;
  tags?: string;
  created_at: string;
  updated_at: string;
}

export interface DashboardMetrics {
  total_tickets: number;
  open_tickets: number;
  in_progress_tickets: number;
  resolved_tickets: number;
  overdue_tickets: number;
  total_trend_percentage: number;
  open_trend_percentage: number;
  in_progress_trend_percentage: number;
  resolved_trend_percentage: number;
  overdue_trend_percentage: number;
  sla_compliance_rate: number;
  sla_compliant_tickets: number;
  sla_total_eligible: number;
}

export interface TicketTrendPoint {
  date: string;
  open: number;
  in_progress: number;
  resolved: number;
  overdue: number;
}

export interface PriorityDistribution {
  priority: string;
  count: number;
  percentage: number;
}

export interface AuditLog {
  id: number;
  actor_id?: number;
  actor_name?: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  changes_json?: string;
  ip_address?: string;
  user_agent?: string;
  created_at: string;
}

export interface Asset {
  id: number;
  asset_tag: string;
  name: string;
  category: 'HARDWARE' | 'SOFTWARE' | 'NETWORK' | 'PERIPHERAL' | 'OTHER';
  model_number?: string;
  serial_number?: string;
  status: 'IN_USE' | 'IN_STOCK' | 'UNDER_REPAIR' | 'RETIRED' | 'LOST';
  assigned_to_user_id?: number;
  assigned_to_user_name?: string;
  department_id?: number;
  department_name?: string;
  location?: string;
  purchase_date?: string;
  warranty_expiry_date?: string;
  purchase_cost?: number;
  vendor_name?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface ChangeRequest {
  id: number;
  change_number: string;
  title: string;
  description: string;
  reason_for_change: string;
  impact_analysis: string;
  rollback_plan: string;
  category: 'INFRASTRUCTURE' | 'SOFTWARE_DEPLOYMENT' | 'SECURITY_PATCH' | 'HARDWARE' | 'DATABASE';
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  status: 'DRAFT' | 'PENDING_APPROVAL' | 'APPROVED' | 'SCHEDULED' | 'IMPLEMENTING' | 'SUCCESSFUL' | 'ROLLED_BACK' | 'REJECTED';
  requester_id: number;
  requester_name: string;
  assigned_cab_lead_id?: number;
  assigned_cab_lead_name?: string;
  scheduled_start_at?: string;
  scheduled_end_at?: string;
  created_at: string;
  updated_at: string;
}

export interface Problem {
  id: number;
  problem_number: string;
  title: string;
  description: string;
  root_cause?: string;
  workaround?: string;
  status: 'OPEN' | 'INVESTIGATING' | 'WORKAROUND_FOUND' | 'KNOWN_ERROR' | 'RESOLVED' | 'CLOSED';
  impact: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  owner_id: number;
  owner_name?: string;
  department_id?: number;
  department_name?: string;
  resolved_at?: string;
  created_at: string;
}

export interface SurveyResponse {
  id: number;
  ticket_id: number;
  ticket_number: string;
  respondent_id: number;
  respondent_name: string;
  rating: number;
  feedback_text?: string;
  agent_id?: number;
  agent_name?: string;
  created_at: string;
}

export interface TimeEntry {
  id: number;
  ticket_id: number;
  ticket_number: string;
  user_id: number;
  user_name: string;
  hours_spent: number;
  activity_type: string;
  description?: string;
  logged_at: string;
}

export interface Vendor {
  id: number;
  name: string;
  code: string;
  contact_name?: string;
  contact_email?: string;
  contact_phone?: string;
  website?: string;
  support_portal?: string;
  sla_notes?: string;
  is_active: boolean;
  rating: number;
  created_at: string;
  updated_at: string;
}

export interface SoftwareLicense {
  id: number;
  vendor_id: number;
  vendor_name?: string;
  software_name: string;
  license_key?: string;
  license_type: 'PERPETUAL' | 'SUBSCRIPTION' | 'PER_USER' | 'SITE';
  total_seats: number;
  allocated_seats: number;
  cost_per_seat: number;
  purchase_date?: string;
  expiry_date?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Contract {
  id: number;
  contract_number: string;
  title: string;
  vendor_id: number;
  vendor_name?: string;
  contract_type: 'SLA_SUPPORT' | 'LEASE' | 'MAINTENANCE' | 'CLOUD_SERVICE';
  status: 'DRAFT' | 'ACTIVE' | 'EXPIRED' | 'RENEWAL_PENDING' | 'TERMINATED';
  annual_cost: number;
  start_date: string;
  end_date: string;
  auto_renew: boolean;
  notice_period_days: number;
  document_url?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface OnCallShift {
  id: number;
  rotation_id: number;
  user_id: number;
  primary_user_name?: string;
  start_at: string;
  end_at: string;
  override_user_id?: number;
  override_user_name?: string;
  notes?: string;
  created_at: string;
}

export interface OnCallRotation {
  id: number;
  name: string;
  department_id: number;
  department_name?: string;
  rotation_type: 'DAILY' | 'WEEKLY' | 'BIWEEKLY' | 'CUSTOM';
  start_time: string;
  time_zone: string;
  is_active: boolean;
  created_at: string;
  shifts: OnCallShift[];
}

export interface ServiceCatalogCategory {
  id: number;
  name: string;
  description?: string;
  icon_name: string;
  display_order: number;
  is_active: boolean;
}

export interface ServiceCatalogItem {
  id: number;
  category_id: number;
  category_name?: string;
  name: string;
  short_description: string;
  full_description?: string;
  estimated_fulfillment_hours: number;
  requires_approval: boolean;
  target_department_id?: number;
  target_department_name?: string;
  is_active: boolean;
  cost: number;
  icon_name: string;
  created_at: string;
}

export interface CustomField {
  id: number;
  name: string;
  field_key: string;
  field_type: 'TEXT' | 'NUMBER' | 'SELECT' | 'CHECKBOX' | 'DATE';
  description?: string;
  is_required: boolean;
  options_json?: string;
  target_entity: 'TICKET' | 'ASSET' | 'CHANGE';
  is_active: boolean;
  display_order: number;
  created_at: string;
}

export interface CustomFieldValue {
  id: number;
  custom_field_id: number;
  custom_field_name?: string;
  entity_id: number;
  field_value?: string;
  created_at: string;
}

export interface EmailTemplate {
  id: number;
  name: string;
  event_trigger: string;
  subject_template: string;
  body_template: string;
  is_active: boolean;
  description?: string;
  created_at: string;
  updated_at: string;
}

