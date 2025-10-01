import type { SelectedFacets } from './FacetPanel'

type Props = {
  selected: SelectedFacets
  onRemove: (facet: keyof SelectedFacets, value: string) => void
  onClear: () => void
}

function AppliedFiltersBar({ selected, onRemove, onClear }: Props) {
  const chips: Array<{ facet: keyof SelectedFacets; value: string }> = []
  Object.entries(selected).forEach(([facet, values]) => {
    ;(values as string[]).forEach(v => chips.push({ facet: facet as keyof SelectedFacets, value: v }))
  })

  if (chips.length === 0) return null

  return (
    <div className="flex gap-2 items-center mb-3">
      <div className="flex gap-2 flex-wrap">
        {chips.map(c => (
          <button
            key={`${c.facet}:${c.value}`}
            onClick={() => onRemove(c.facet, c.value)}
            className="chip hover:bg-gray-200 dark:hover:bg-gray-700"
            aria-label={`Filter entfernen ${c.facet} ${c.value}`}
          >
            <strong className="mr-2 text-xs text-gray-500 dark:text-gray-500">{(() => {
              switch (c.facet) {
                case 'location': return 'Ort'
                case 'band': return 'Band'
                case 'status_kind': return 'Status'
                case 'weekday': return 'Wochentag'
                default: return c.facet
              }
            })()}:</strong>
            <span className="truncate max-w-xs">{(() => {
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
            })()}</span>
          </button>
        ))}
      </div>
      <div className="ml-auto">
        <button onClick={onClear} className="text-sm text-gray-500 dark:text-gray-500">Alle löschen</button>
      </div>
    </div>
  )
}

export default AppliedFiltersBar;