import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateString?: string): string {
  if (!dateString) return "N/A";
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return dateString;
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

export function formatTimeAgo(dateString?: string): string {
  if (!dateString) return "";
  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (seconds < 60) return "Just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 30) return `${days}d ago`;
  return formatDate(dateString);
}

export function formatTimeRemaining(targetDateString?: string): { text: string; isBreached: boolean; isWarning: boolean } {
  if (!targetDateString) return { text: "No SLA set", isBreached: false, isWarning: false };
  const target = new Date(targetDateString);
  const now = new Date();
  const diffMs = target.getTime() - now.getTime();

  if (diffMs <= 0) {
    const pastMinutes = Math.abs(Math.floor(diffMs / (1000 * 60)));
    if (pastMinutes < 60) return { text: `Breached ${pastMinutes}m ago`, isBreached: true, isWarning: false };
    const pastHours = Math.floor(pastMinutes / 60);
    return { text: `Breached ${pastHours}h ago`, isBreached: true, isWarning: false };
  }

  const remainingMinutes = Math.floor(diffMs / (1000 * 60));
  if (remainingMinutes < 60) {
    return { text: `${remainingMinutes}m remaining`, isBreached: false, isWarning: remainingMinutes < 30 };
  }
  const remainingHours = Math.floor(remainingMinutes / 60);
  const remainingMinsRem = remainingMinutes % 60;
  return { text: `${remainingHours}h ${remainingMinsRem}m remaining`, isBreached: false, isWarning: remainingHours < 2 };
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
}
