
function weekdayShortDe(date: Date): string {
  const days = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa']
  return days[date.getDay()] || ''
}

function monthShortDe(date: Date): string {
  // German short month names (3 letters where applicable)
  const months = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
  return months[date.getMonth()] || ''
}

function LeadingTile({ date }: { date: string | number | Date | null | undefined }) {
  let d: Date | null = null
  try {
    if (date == null || date === '') d = null
    else d = new Date(date as any)
    if (d && isNaN(d.getTime())) d = null
  } catch (e) {
    d = null
  }

  const weekday = d ? weekdayShortDe(d) : ''
  const day = d ? String(d.getDate()) : ''
  const month = d ? monthShortDe(d) : ''

  const ariaLabel = d ? `${weekday} ${day}. ${month}` : 'Datum unbekannt'

  return (
    <div
      role="img"
      aria-label={ariaLabel}
      style={{
        width: 64,
        minWidth: 64,
        height: 64,
        borderRadius: 8,
        background: '#f0f4ff',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        boxShadow: 'inset 0 -1px 0 rgba(0,0,0,0.02)'
      }}
    >
      <div style={{ fontSize: 12, color: 'var(--text)', opacity: 0.9 }}>{weekday}</div>
      <div style={{ fontSize: 20, fontWeight: 700, lineHeight: '20px', color: 'var(--text)' }}>{day}</div>
      <div style={{ fontSize: 12, color: 'var(--text)', opacity: 0.9 }}>{month}</div>
    </div>
  )
}

export default LeadingTile;
