import React from 'react'

function displayStatusLabel(status?: string) {
  if (!status) return ''
  // basic normalization: capitalize first letter
  return status.charAt(0).toUpperCase() + status.slice(1)
}

export default function StatusTile({ status }: { status?: string }) {
  const label = displayStatusLabel(status)
  return (
    <div style={{ width: 28, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div
        aria-label={label || 'Status'}
        title={label}
        style={{
          transform: 'rotate(-90deg)',
          transformOrigin: 'center',
          fontSize: 12,
          color: 'var(--text)',
          background: '#6b7280',
          padding: '4px 6px',
          borderRadius: 4,
          whiteSpace: 'nowrap',
          display: 'inline-block'
        }}
      >
        {label}
      </div>
    </div>
  )
}
