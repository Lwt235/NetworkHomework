/**
 * Utility functions for the frontend
 */

/**
 * Format bytes to human-readable string
 * @param {number} bytes - The number of bytes
 * @returns {string} Formatted string like "1.5 MB"
 */
export function formatBytes(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

/**
 * Format timestamp to localized string
 * @param {string|Date} timestamp - The timestamp to format
 * @param {string} locale - The locale to use (default: 'zh-CN')
 * @returns {string} Formatted date string
 */
export function formatTime(timestamp, locale = 'zh-CN') {
  return new Date(timestamp).toLocaleString(locale, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
