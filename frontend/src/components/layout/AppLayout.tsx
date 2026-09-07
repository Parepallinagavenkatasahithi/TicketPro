import React, { useState } from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { GlobalSearchModal } from '../ui/GlobalSearchModal';
import { CreateTicketModal } from '../../features/tickets/CreateTicketModal';
import { cn } from '../../lib/utils';

interface AppLayoutProps {
  children: React.ReactNode;
}

export const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isCreateTicketOpen, setIsCreateTicketOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background text-text-primary flex">
      {/* Sidebar */}
      <Sidebar
        collapsed={collapsed}
        onToggleCollapse={() => setCollapsed(!collapsed)}
        onCreateTicketClick={() => setIsCreateTicketOpen(true)}
      />

      {/* Main Content Area */}
      <div
        className={cn(
          'flex-1 flex flex-col min-w-0 transition-all duration-300',
          collapsed ? 'ml-20' : 'ml-64'
        )}
      >
        {/* Top Header */}
        <Header
          onToggleSidebar={() => setCollapsed(!collapsed)}
          onOpenSearch={() => setIsSearchOpen(true)}
        />

        {/* Dynamic Page Content */}
        <main className="flex-1 p-4 sm:p-6 md:p-8 max-w-7xl w-full mx-auto">
          {children}
        </main>
      </div>

      {/* Global Search Dialog */}
      <GlobalSearchModal isOpen={isSearchOpen} onClose={() => setIsSearchOpen(false)} />

      {/* Ticket Creation Modal */}
      <CreateTicketModal isOpen={isCreateTicketOpen} onClose={() => setIsCreateTicketOpen(false)} />
    </div>
  );
};
