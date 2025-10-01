import React from 'react'
import useDarkMode from '../hooks/useDarkMode'

export default function DarkModeToggle() {
  const { isDark, setIsDark } = useDarkMode()
  return (
    <button
      onClick={() => setIsDark(!isDark)}
      aria-pressed={isDark}
      className="hidden ml-4 inline-flex items-center gap-2 px-3 py-1 rounded border bg-white dark:bg-gray-800 text-sm"
      title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
    >
      <span className="sr-only">Toggle dark mode</span>
      {isDark ? '🌙 Dark' : '☀️ Light'}
    </button>
  )
}
