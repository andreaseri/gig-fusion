// import { useState, useEffect, useRef } from 'react'
import { useState, useEffect } from 'react'
import FacetPanel, { type SelectedFacets } from './FacetPanel'
import LeadingTile from './LeadingTile'
import InfoTile from './InfoTile'
import AppliedFiltersBar from './AppliedFiltersBar'
import StatusTile from './StatusTile'

type SearchResult = any

function JsonBlock({ data }: { data: any }) {
  return (
    <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word', background: '#f6f8fa', padding: 12, borderRadius: 6 }}>
      {JSON.stringify(data, null, 2)}
    </pre>
  )
}

function Search() {
  const [q, setQ] = useState<string>('')
  // const [limit, setLimit] = useState<number>(1000)
  const [limit] = useState<number>(1000)
  const [res, setRes] = useState<SearchResult | null>(null)
  // const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const emptySelected = { location: [], band: [], status_kind: [], weekday: [] } as SelectedFacets
  const [selected, setSelected] = useState<SelectedFacets>(emptySelected)
  // const rootRef = useRef<HTMLDivElement | null>(null)
  const [facetsResetKey, setFacetsResetKey] = useState<number>(0)
  const [rawExpanded, setRawExpanded] = useState<boolean>(false)

  async function doSearch(overrides?: SelectedFacets, limitOverride?: number) {
    setError(null)
    // setLoading(true)
    setRes(null)
    try {
      const metaEnv = (import.meta as any).env || {}
      const base = metaEnv.VITE_BACKEND_URL || 'http://localhost:8000'
      const useSel = overrides ?? selected
      const filter = buildFilter(useSel)
      const useLimit = typeof limitOverride === 'number' ? limitOverride : limit
      const weekdayParam = (useSel.weekday && useSel.weekday.length) ? `&weekday=${encodeURIComponent(useSel.weekday.join(','))}` : ''
      const url = `${base}/search?q=${encodeURIComponent(q)}&limit=${useLimit}${filter ? `&filter=${encodeURIComponent(filter)}` : ''}${weekdayParam}`
      const r = await fetch(url)
      const j = await r.json()
      setRes(j)
    } catch (err: any) {
      setError(err?.message || String(err))
    } finally {
      // setLoading(false)
    }
  }

 

  // Run an initial search when the component mounts
  useEffect(() => {
    // Reset filters & facet view state on initial load, and request a larger
    // limit so the facet distribution is populated with many values.
    setSelected(emptySelected)
    setFacetsResetKey(k => k + 1)
    void doSearch(emptySelected, 1000)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // Debounced auto-search when typing in the query input
  useEffect(() => {
    const id = setTimeout(() => {
      ;(async () => {
        // If the query is empty, treat this as a reset: clear selected
        // facets and reset the facet panel view state, then fetch initial data.
        if (q.trim() === '') {
          setSelected(emptySelected)
          setFacetsResetKey(k => k + 1)
          await doSearch(emptySelected)
          return
        }

        // Otherwise perform the normal debounced search
        await doSearch()
      })()
    }, 250)
    return () => clearTimeout(id)
    // only trigger when query changes; toggles call doSearch immediately
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q])

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key !== 'Enter') return
      const active = document.activeElement
      if (!active) return
      const tag = active.tagName.toLowerCase()
      const isInputLike = tag === 'input' || tag === 'textarea' || (active as HTMLElement).isContentEditable
      if (isInputLike) {
        // If the focused element is an input, let the native form submit/handlers run
        return
      }
      // Otherwise trigger a search
      void doSearch()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [doSearch])

  function buildFilter(sel: SelectedFacets): string {
    const parts: string[] = []
    if (sel.location.length) {
      parts.push(`(${sel.location.map(v => `location = "${v.replace(/"/g, '\\"')}"`).join(' OR ')})`)
    }
    if (sel.band.length) {
      parts.push(`(${sel.band.map(v => `band = "${v.replace(/"/g, '\\"')}"`).join(' OR ')})`)
    }
    if (sel.status_kind.length) {
      parts.push(`(${sel.status_kind.map(v => `status_kind = "${v.replace(/"/g, '\\"')}"`).join(' OR ')})`)
    }
    return parts.join(' AND ')
  }

  // function formatDate(val: any): string {
  //   if (!val) return ''
  //   const asDate = new Date(val)
  //   if (!isNaN(asDate.getTime())) {
  //     const dd = String(asDate.getDate()).padStart(2, '0')
  //     const mm = String(asDate.getMonth() + 1).padStart(2, '0')
  //     const yyyy = asDate.getFullYear()
  //     return `${dd}.${mm}.${yyyy}`
  //   }
  //   // fallback for strings like YYYY-MM-DD
  //   const m = String(val).match(/(\d{4})-(\d{2})-(\d{2})/)
  //   if (m) return `${m[3]}.${m[2]}.${m[1]}`
  //   return String(val)
  // }

  function onToggle(facetName: keyof SelectedFacets, value: string) {
    const current = selected[facetName]
    const exists = current.includes(value)
    const newSelected = { ...selected, [facetName]: exists ? current.filter(v => v !== value) : [...current, value] }
    setSelected(newSelected)
    void doSearch(newSelected)
  }

  function onRemove(facetName: keyof SelectedFacets, value: string) {
    const newSelected = { ...selected, [facetName]: selected[facetName].filter(v => v !== value) }
    setSelected(newSelected)
    void doSearch(newSelected)
  }

  return (
    <div className="w-full">
      <div className="w-full max-w-[1200px] mx-auto flex gap-4">
        <FacetPanel
          distribution={res?.facets ?? null}
          selected={selected}
          onToggle={onToggle}
          onClear={() => {
            const empty = { location: [], band: [], status_kind: [], weekday: [] } as SelectedFacets
            setSelected(empty)
            setFacetsResetKey(k => k + 1)
            void doSearch(empty)
          }}
          resetKey={facetsResetKey}
        />

        <div className="flex-1">
          <form
            onSubmit={(e) => {
              e.preventDefault()
              if (q.trim() === '') {
                setSelected(emptySelected)
                setFacetsResetKey(k => k + 1)
                void doSearch(emptySelected)
              } else {
                void doSearch()
              }
            }}
            className="flex gap-2 mb-2"
          >
            <div className="relative flex-1">
              <input
                className="input-base text-lg pr-10"
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder="Suche (z. B. sonic)"
                aria-label="Suche"
              />
              {q && (
                <button
                  type="button"
                  onClick={() => {
                    setQ('')
                    setSelected(emptySelected)
                    setFacetsResetKey(k => k + 1)
                    void doSearch(emptySelected)
                  }}
                  aria-label="Clear search"
                  className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                >
                  ×
                </button>
              )}
            </div>

            {/* <button type="submit" disabled={loading} className="px-3 py-2">{loading ? 'Searching…' : 'Search'}</button> */}
          </form>

          <AppliedFiltersBar selected={selected} onRemove={onRemove} onClear={() => { const empty = { location: [], band: [], status_kind: [], weekday: [] } as SelectedFacets; setSelected(empty); setFacetsResetKey(k => k + 1); void doSearch(empty) }} />

          {error && <div className="text-red-600 mb-2">{error}</div>}

          {res ? (
            <div>
              {Array.isArray(res.hits) && res.hits.length === 0 ? (
                <div className="p-5 text-center text-gray-600">
                  <div className="text-4xl mb-2">😕</div>
                  <div className="text-lg font-semibold mb-1">Keine Treffer</div>
                  <div className="mb-3">Für Ihre Suche wurden keine Ergebnisse gefunden.</div>
                  <div className="flex gap-2 justify-center">
                    <button
                      type="button"
                      onClick={() => {
                        setQ('')
                        const empty = { location: [], band: [], status_kind: [], weekday: [] } as SelectedFacets
                        setSelected(empty)
                        setFacetsResetKey(k => k + 1)
                        void doSearch(empty)
                      }}
                      className="px-3 py-2 border rounded"
                    >
                      Filter zurücksetzen
                    </button>
                  </div>
                </div>
              ) : (
                <div>
                  <div className="mb-3">
                    {Array.isArray(res.hits) && res.hits.slice(0, limit).map((h: any) => (
                      <div key={h.id} className="flex flex-col">
                        <div className="p-2 border-b border-gray-100 grid grid-cols-[64px_1fr] gap-3 items-center">
                          <div className="flex items-center justify-center">
                            <LeadingTile date={h.date} />
                          </div>
                          <div>
                            <InfoTile band={h.band} location={h.location} price_eur={h.price_eur} status_kind={h.status_kind} />
                          </div>
                        </div>
                        <div className="hidden">
                          <StatusTile status={h.status_kind} />
                        </div>
                      </div>
                    ))}
                  </div>

                  <div
                    role="button"
                    tabIndex={0}
                    onClick={() => setRawExpanded(v => !v)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault()
                        setRawExpanded(v => !v)
                      }
                    }}
                    aria-pressed={rawExpanded}
                    aria-label={rawExpanded ? 'Raw data einklappen' : 'Raw data anzeigen'}
                    className="flex items-center justify-between cursor-pointer"
                  >
                    <h4 className="m-0">Raw data</h4>
                    <span className="text-lg">{rawExpanded ? '▲' : '▼'}</span>
                  </div>
                  {rawExpanded && <JsonBlock data={res} />}
                </div>
              )}
            </div>
          ) : (
            <div aria-hidden={true} className="text-gray-600" />
          )}
        </div>
      </div>
    </div>
  )
}

 export default Search;