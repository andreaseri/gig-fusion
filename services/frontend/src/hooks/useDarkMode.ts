import { useEffect, useState } from 'react'

const KEY = 'gigfusion:color-scheme'

export default function useDarkMode() {
  const [isDark, setIsDark] = useState<boolean>(() => {
    try {
      // skip dark mode for now
      return false;

      const stored = localStorage.getItem(KEY)
      if (stored) return stored === 'dark'
      return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
    } catch (e) {
      return false
    }
  })

  useEffect(() => {
    try {
      const root = document.documentElement
      if (isDark) root.classList.add('dark')
      else root.classList.remove('dark')
      localStorage.setItem(KEY, isDark ? 'dark' : 'light')
    } catch (e) {
      // ignore
    }
  }, [isDark])

  return { isDark, setIsDark }
}
