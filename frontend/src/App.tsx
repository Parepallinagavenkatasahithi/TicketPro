import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { AppLayout } from './components/layout/AppLayout';
import { LoginPage } from './features/auth/LoginPage';
import { DashboardPage } from './features/dashboard/DashboardPage';
import { TicketListPage } from './features/tickets/TicketListPage';
import { TicketDetailPage } from './features/tickets/TicketDetailPage';
import { EmployeeListPage } from './features/employees/EmployeeListPage';
import { DepartmentListPage } from './features/departments/DepartmentListPage';
import { ApprovalListPage } from './features/approvals/ApprovalListPage';
import { AnnouncementListPage } from './features/announcements/AnnouncementListPage';
import { KBPage } from './features/knowledge-base/KBPage';
import { SLAManagementPage } from './features/sla/SLAManagementPage';
import { AnalyticsPage } from './features/analytics/AnalyticsPage';
import { AuditLogPage } from './features/audit/AuditLogPage';
import { SettingsPage } from './features/settings/SettingsPage';
import { AssetListPage } from './features/assets/AssetListPage';
import { ChangeRequestListPage } from './features/change-requests/ChangeRequestListPage';
import { ProblemListPage } from './features/problems/ProblemListPage';
import { SurveyListPage } from './features/surveys/SurveyListPage';
import { TimeTrackingPage } from './features/time-tracking/TimeTrackingPage';
import { VendorListPage } from './features/vendors/VendorListPage';
import { ContractListPage } from './features/contracts/ContractListPage';
import { OnCallPage } from './features/on-call/OnCallPage';
import { ServiceCatalogPage } from './features/service-catalog/ServiceCatalogPage';
import { CustomFieldsPage } from './features/custom-fields/CustomFieldsPage';
import { EmailTemplatesPage } from './features/email-templates/EmailTemplatesPage';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isLoading } = useAuth();
  if (isLoading) return <div className="p-12 text-center text-xs text-text-tertiary">Loading TicketPro...</div>;
  if (!user) return <Navigate to="/login" replace />;
  return <AppLayout>{children}</AppLayout>;
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          <Route path="/tickets" element={<ProtectedRoute><TicketListPage /></ProtectedRoute>} />
          <Route path="/my-tickets" element={<ProtectedRoute><TicketListPage /></ProtectedRoute>} />
          <Route path="/tickets/:id" element={<ProtectedRoute><TicketDetailPage /></ProtectedRoute>} />

          <Route path="/employees" element={<ProtectedRoute><EmployeeListPage /></ProtectedRoute>} />
          <Route path="/departments" element={<ProtectedRoute><DepartmentListPage /></ProtectedRoute>} />
          <Route path="/roles" element={<ProtectedRoute><EmployeeListPage /></ProtectedRoute>} />

          <Route path="/assets" element={<ProtectedRoute><AssetListPage /></ProtectedRoute>} />
          <Route path="/change-requests" element={<ProtectedRoute><ChangeRequestListPage /></ProtectedRoute>} />
          <Route path="/problems" element={<ProtectedRoute><ProblemListPage /></ProtectedRoute>} />
          <Route path="/surveys" element={<ProtectedRoute><SurveyListPage /></ProtectedRoute>} />
          <Route path="/time-tracking" element={<ProtectedRoute><TimeTrackingPage /></ProtectedRoute>} />
          <Route path="/vendors" element={<ProtectedRoute><VendorListPage /></ProtectedRoute>} />
          <Route path="/contracts" element={<ProtectedRoute><ContractListPage /></ProtectedRoute>} />
          <Route path="/on-call" element={<ProtectedRoute><OnCallPage /></ProtectedRoute>} />
          <Route path="/service-catalog" element={<ProtectedRoute><ServiceCatalogPage /></ProtectedRoute>} />
          <Route path="/custom-fields" element={<ProtectedRoute><CustomFieldsPage /></ProtectedRoute>} />
          <Route path="/email-templates" element={<ProtectedRoute><EmailTemplatesPage /></ProtectedRoute>} />

          <Route path="/approvals" element={<ProtectedRoute><ApprovalListPage /></ProtectedRoute>} />
          <Route path="/announcements" element={<ProtectedRoute><AnnouncementListPage /></ProtectedRoute>} />
          <Route path="/knowledge-base" element={<ProtectedRoute><KBPage /></ProtectedRoute>} />
          <Route path="/knowledge-base/:slug" element={<ProtectedRoute><KBPage /></ProtectedRoute>} />
          <Route path="/sla" element={<ProtectedRoute><SLAManagementPage /></ProtectedRoute>} />
          <Route path="/analytics" element={<ProtectedRoute><AnalyticsPage /></ProtectedRoute>} />
          <Route path="/audit" element={<ProtectedRoute><AuditLogPage /></ProtectedRoute>} />
          <Route path="/settings" element={<ProtectedRoute><SettingsPage /></ProtectedRoute>} />
          <Route path="/integrations" element={<ProtectedRoute><SettingsPage /></ProtectedRoute>} />

          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
};
