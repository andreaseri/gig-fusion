import React, { useEffect, useState } from 'react'

export type FacetValue = { value: string; count: number }

export type FacetDistribution = Record<string, FacetValue[] | undefined>

export type SelectedFacets = {
  location: string[]
  band: string[]
  status_kind: string[]
  weekday: string[]
  // price handled separately
}

export type FacetPanelProps = {
  distribution: Record<string, Record<string, number> | undefined> | null
  selected: SelectedFacets
  onToggle: (facetName: keyof SelectedFacets, value: string) => void
  onClear: () => void
  resetKey?: number
}

function valuesFromDist(dist?: Record<string, number>) {
  if (!dist) return [] as FacetValue[]
  return Object.entries(dist).map(([value, count]) => ({ value, count }))
}

type FacetKeys = 'location' | 'band' | 'status_kind' | 'weekday'


export default function FacetPanel({ distribution, selected, onToggle, onClear, resetKey }: FacetPanelProps) {
  // Keep last-seen counts per facet value so numbers don't jump when filters change.
  const weekdayOrder = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
  const orderIndex = (v: string) => {
    const idx = weekdayOrder.indexOf(v.toLowerCase())
    return idx === -1 ? 999 : idx
  }
  const [seenCounts, setSeenCounts] = useState<Record<FacetKeys, Map<string, number>>>(() => ({
    location: new Map(),
    band: new Map(),
    status_kind: new Map(),
    weekday: new Map(),
  }))
  const [showCounts, setShowCounts] = useState<Record<FacetKeys, number>>(() => ({ location: 10, band: 10, status_kind: 10, weekday: 10 }))

  useEffect(() => {
    setSeenCounts(prev => {
      const next: Record<FacetKeys, Map<string, number>> = {
        location: new Map(prev.location),
        band: new Map(prev.band),
        status_kind: new Map(prev.status_kind),
        weekday: new Map(prev.weekday),
      }
      ;(Object.keys(distribution || {}) as string[]).forEach(kRaw => {
        const k = kRaw as FacetKeys
        if (!(k in next)) return
        const values = distribution?.[k] as Record<string, number> | undefined
        if (values) {
          Object.entries(values).forEach(([v, count]) => next[k].set(v, count))
        }
      })
      return next
    })
  }, [distribution])

  // reset view state when parent requests it (e.g. Clear from search bar)
  useEffect(() => {
    setShowCounts({ location: 10, band: 10, status_kind: 10, weekday: 10 })
  }, [resetKey])

  function renderList(key: FacetKeys) {
    const dist = distribution?.[key] as Record<string, number> | undefined
      const selectedVals = selected[key] || []
      const keysSet = new Set<string>([...Array.from(seenCounts[key].keys()), ...(dist ? Object.keys(dist) : []), ...selectedVals])
    const values = Array.from(keysSet)
    // For the weekday facet, sort by natural week order; otherwise alphabetical
    const weekdayOrder = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    const orderIndex = (v: string) => {
      const idx = weekdayOrder.indexOf(v.toLowerCase())
      return idx === -1 ? 999 : idx
    }
    values.sort((a, b) => {
      if (key === 'weekday') return orderIndex(a) - orderIndex(b)
      return a.localeCompare(b)
    })
    return values.map(v => {
      const seen = seenCounts[key].get(v)
      const current = dist?.[v]
      const displayCount = seen ?? current ?? 0
      const isPresentNow = !!current && current > 0
        return { value: v, count: displayCount, presentNow: isPresentNow }
    })
  }

  function visibleItemsFor(key: FacetKeys) {
    const all = renderList(key)
    const total = all.length
    const shown = showCounts[key]
    // If expanded, still apply the same ordering rules as the collapsed view
    // (selected first, then present unselected, then absent unselected).
    
    if (shown >= total) {
      const selectedVals = selected[key] || []
      const selectedSet = new Set(selectedVals)
      const selectedItems = all.filter(a => selectedSet.has(a.value))
      const unselected = all.filter(a => !selectedSet.has(a.value))
      const presentUnselected = unselected.filter(a => a.presentNow).sort((a, b) => {
        if (key === 'weekday') return orderIndex(a.value) - orderIndex(b.value)
        return a.value.localeCompare(b.value)
      })
      const absentUnselected = unselected.filter(a => !a.presentNow).sort((a, b) => {
        if (key === 'weekday') return orderIndex(a.value) - orderIndex(b.value)
        return a.value.localeCompare(b.value)
      })
      return [...selectedItems, ...presentUnselected, ...absentUnselected]
    }

    const selectedVals = selected[key] || []
    const selectedSet = new Set(selectedVals)
    const selectedItems = all.filter(a => selectedSet.has(a.value))

    // if more than the collapsed limit selected, show all selected
    if (selectedItems.length > shown) return selectedItems

    // otherwise show selected first, then present (applicable) unselected items alphabetically,
    // then absent unselected items to fill up to 'shown'
    const unselected = all.filter(a => !selectedSet.has(a.value))
    const presentUnselected = unselected.filter(a => a.presentNow).sort((a, b) => {
      if (key === 'weekday') return orderIndex(a.value) - orderIndex(b.value)
      return a.value.localeCompare(b.value)
    })
    const absentUnselected = unselected.filter(a => !a.presentNow).sort((a, b) => {
      if (key === 'weekday') return orderIndex(a.value) - orderIndex(b.value)
      return a.value.localeCompare(b.value)
    })
    const fillers: typeof all = [...presentUnselected, ...absentUnselected].slice(0, Math.max(0, shown - selectedItems.length))
    return [...selectedItems, ...fillers]
  }

  return (
    <aside style={{ width: 260, paddingRight: 12 }}>
      <div style={{ marginBottom: 12 }}>
        <strong>Filter</strong>
        <div style={{ marginTop: 6 }}>
          <button
            onClick={() => {
              setShowCounts({ location: 10, band: 10, status_kind: 10, weekday: 10 })
              onClear()
            }}
            style={{ fontSize: 12 }}
          >
            Alle löschen
          </button>
        </div>
      </div>

      <div style={{ marginBottom: 12 }}>
        <h5>
          Ort
          {(() => {
            const all = renderList('location')
            const applicable = all.filter(a => a.presentNow && !selected.location.includes(a.value)).length
            return applicable > 0 ? <small style={{ marginLeft: 8, color: '#0a66c2' }}>+{applicable}</small> : null
          })()}
        </h5>
        {visibleItemsFor('location').map(v => (
          <label key={v.value} style={{ display: 'block', opacity: v.presentNow ? 1 : 0.5 }}>
            <input type="checkbox" checked={selected.location.includes(v.value)} onChange={() => onToggle('location', v.value)} /> {v.value} <small>({v.count})</small>
          </label>
        ))}
        {renderList('location').length > 10 && (
          <div>
            <button style={{ fontSize: 12 }} onClick={() => setShowCounts(prev => ({ ...prev, location: prev.location === 10 ? renderList('location').length : 10 }))}>
              {showCounts.location === 10 ? 'Mehr anzeigen' : 'Weniger anzeigen'}
            </button>
          </div>
        )}
      </div>

      <div style={{ marginBottom: 12 }}>
        <h5>
          Band
          {(() => {
            const all = renderList('band')
            const applicable = all.filter(a => a.presentNow && !selected.band.includes(a.value)).length
            return applicable > 0 ? <small style={{ marginLeft: 8, color: '#0a66c2' }}>+{applicable}</small> : null
          })()}
        </h5>
        {visibleItemsFor('band').map(v => (
          <label key={v.value} style={{ display: 'block', opacity: v.presentNow ? 1 : 0.5 }}>
            <input type="checkbox" checked={selected.band.includes(v.value)} onChange={() => onToggle('band', v.value)} /> {v.value} <small>({v.count})</small>
          </label>
        ))}
        {renderList('band').length > 10 && (
          <div>
            <button style={{ fontSize: 12 }} onClick={() => setShowCounts(prev => ({ ...prev, band: prev.band === 10 ? renderList('band').length : 10 }))}>
              {showCounts.band === 10 ? 'Mehr anzeigen' : 'Weniger anzeigen'}
            </button>
          </div>
        )}
      </div>

      <div style={{ marginBottom: 12 }}>
        <h5>
          Wochentag
          {(() => {
            const all = renderList('weekday')
            const applicable = all.filter(a => a.presentNow && !(selected.weekday || []).includes(a.value)).length
            return applicable > 0 ? <small style={{ marginLeft: 8, color: '#0a66c2' }}>+{applicable}</small> : null
          })()}
        </h5>
        {visibleItemsFor('weekday').map(v => {
          const weekdayMap: Record<string, string> = {
            mon: 'Mo',
            tue: 'Di',
            wed: 'Mi',
            thu: 'Do',
            fri: 'Fr',
            sat: 'Sa',
            sun: 'So',
            // full names/fallbacks
            monday: 'Mo',
            tuesday: 'Di',
            wednesday: 'Mi',
            thursday: 'Do',
            friday: 'Fr',
            saturday: 'Sa',
            sunday: 'So',
          }
          const display = weekdayMap[v.value.toLowerCase()] ?? v.value
          return (
            <label key={v.value} style={{ display: 'block', opacity: v.presentNow ? 1 : 0.5 }}>
              <input type="checkbox" checked={(selected.weekday || []).includes(v.value)} onChange={() => onToggle('weekday', v.value)} /> {display} <small>({v.count})</small>
            </label>
          )
        })}
        {renderList('weekday').length > 10 && (
          <div>
            <button style={{ fontSize: 12 }} onClick={() => setShowCounts(prev => ({ ...prev, weekday: prev.weekday === 10 ? renderList('weekday').length : 10 }))}>
              {showCounts.weekday === 10 ? 'Mehr anzeigen' : 'Weniger anzeigen'}
            </button>
          </div>
        )}
      </div>

      <div style={{ marginBottom: 12 }}>
        <h5>
          Status
          {(() => {
            const all = renderList('status_kind')
            const applicable = all.filter(a => a.presentNow && !selected.status_kind.includes(a.value)).length
            return applicable > 0 ? <small style={{ marginLeft: 8, color: '#0a66c2' }}>+{applicable}</small> : null
          })()}
        </h5>
        {visibleItemsFor('status_kind').map(v => (
          <label key={v.value} style={{ display: 'block', opacity: v.presentNow ? 1 : 0.5 }}>
            <input type="checkbox" checked={selected.status_kind.includes(v.value)} onChange={() => onToggle('status_kind', v.value)} /> {v.value} <small>({v.count})</small>
          </label>
        ))}
        {renderList('status_kind').length > 10 && (
          <div>
            <button style={{ fontSize: 12 }} onClick={() => setShowCounts(prev => ({ ...prev, status_kind: prev.status_kind === 10 ? renderList('status_kind').length : 10 }))}>
              {showCounts.status_kind === 10 ? 'Mehr anzeigen' : 'Weniger anzeigen'}
            </button>
          </div>
        )}
      </div>
    </aside>
  )
}
