import React from 'react'
import type { SelectedFacets } from './FacetPanel'

type Props = {
  selected: SelectedFacets
  onRemove: (facet: keyof SelectedFacets, value: string) => void
  onClear: () => void
}

export default function AppliedFiltersBar({ selected, onRemove, onClear }: Props) {
  const chips: Array<{ facet: keyof SelectedFacets; value: string }> = []
  Object.entries(selected).forEach(([facet, values]) => {
    ;(values as string[]).forEach(v => chips.push({ facet: facet as keyof SelectedFacets, value: v }))
  })

  if (chips.length === 0) return null

  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 12 }}>
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        {chips.map(c => (
          <button
            key={`${c.facet}:${c.value}`}
            onClick={() => onRemove(c.facet, c.value)}
            style={{ background: '#eee', border: 'none', padding: '6px 8px', borderRadius: 16, cursor: 'pointer' }}
            aria-label={`Filter entfernen ${c.facet} ${c.value}`}
          >
            <strong style={{ marginRight: 6 }}>{(() => {
              switch (c.facet) {
                case 'location': return 'Ort'
                case 'band': return 'Band'
                case 'status_kind': return 'Status'
                case 'weekday': return 'Wochentag'
                default: return c.facet
              }
            })()}:</strong> {(() => {
              if (c.facet === 'weekday') {
                const weekdayMap: Record<string, string> = {
                  mon: 'Mo',
                  tue: 'Di',
                  wed: 'Mi',
                  thu: 'Do',
                  fri: 'Fr',
                  sat: 'Sa',
                  sun: 'So',
                  monday: 'Mo',
                  tuesday: 'Di',
                  wednesday: 'Mi',
                  thursday: 'Do',
                  friday: 'Fr',
                  saturday: 'Sa',
                  sunday: 'So',
                }
                return weekdayMap[c.value.toLowerCase()] ?? c.value
              }
              return c.value
            })()} 
          </button>
        ))}
      </div>
      <div style={{ marginLeft: 'auto' }}>
        <button onClick={onClear} style={{ fontSize: 12 }}>Alle löschen</button>
      </div>
    </div>
  )
}
